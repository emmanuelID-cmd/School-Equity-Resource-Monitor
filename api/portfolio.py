"""Vercel-compatible portfolio API.

The handler joins attendance and graduation rows before paginating schools so the
browser never receives a partial school-year record.
"""
import json
import os
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from src.data.normalize import API_URL, audit_rows

_cache = None
BOROUGH_ORDER = {'Brooklyn': 0, 'Bronx': 1, 'Manhattan': 2, 'Queens': 3, 'Staten Island': 4}


def _load_pairs():
    global _cache
    if _cache is not None:
        return _cache
    snapshot = Path(__file__).parents[1] / 'data' / 'portfolio-snapshot.json'
    if snapshot.exists():
        _cache = json.loads(snapshot.read_text()).get('records', [])
        return _cache
    where = "school_type='High School' AND (metric_display_name like '4-Year Graduation Rate%' OR metric_display_name like 'Percentage of Students with 90%+ Attendance%')"
    rows, offset, page_size = [], 0, 50000
    while True:
        params = urllib.parse.urlencode({'$limit': page_size, '$offset': offset, '$where': where})
        with urllib.request.urlopen(f'{API_URL}?{params}', timeout=60) as response:
            page = json.load(response)
        rows.extend(page)
        if len(page) < page_size:
            break
        offset += page_size
    _cache = audit_rows(rows)['pairs']
    return _cache


def _query(request):
    query = getattr(request, 'args', None) or getattr(request, 'query', None) or {}
    if hasattr(query, 'get'):
        return query
    return {}


def portfolio_response(request):
    try:
        query = _query(request)
        year = query.get('year', '')
        borough = query.get('borough', '')
        dbn = query.get('dbn', '').strip().upper()
        dbn_prefix = query.get('dbn_prefix', '').strip().upper()
        school_name = query.get('school_name', '').strip().lower()
        signal = query.get('signal', 'all')
        directory = query.get('directory', '') == 'latest'
        gap_threshold = float(query.get('gap', 0) or 0)
        limit = min(max(int(query.get('limit', 100)), 1), 100)
        cursor = query.get('cursor', '')
        pairs = [p for p in _load_pairs() if (not year or p['schoolYear'] == year) and (not borough or p['borough'] == borough) and (not dbn or p['dbn'] == dbn) and (not dbn_prefix or p['dbn'].startswith(dbn_prefix)) and (not school_name or school_name in p.get('schoolName', '').lower())]
        schools = {}
        for pair in pairs:
            key = f"{pair['dbn']}|{pair['schoolYear']}"
            school = schools.setdefault(key, {**pair, 'signals': [], 'evidence': []})
            if pair.get('graduation') and pair.get('value') is not None and pair['graduation'].get('value') is not None:
                evidence = {**pair, 'gap': abs(pair['graduation']['value'] - pair['value'])}
                school['evidence'].append(evidence)
                if (pair.get('denominator') or 0) >= 10 and (pair['graduation'].get('denominator') or 0) >= 10 and evidence['gap'] >= 0.05:
                    school['signals'].append(evidence)
            warnings = []
            if pair.get('value') is None: warnings.append('Attendance value missing or suppressed')
            if pair.get('denominator') is not None and pair.get('denominator', 0) < 10: warnings.append('Attendance denominator below 10')
            graduation = pair.get('graduation') or {}
            if not graduation: warnings.append('Graduation record missing for this school year')
            elif graduation.get('value') is None: warnings.append('Graduation value missing or suppressed')
            elif graduation.get('denominator') is not None and graduation.get('denominator', 0) < 10: warnings.append('Graduation denominator below 10')
            school.setdefault('warnings', []).extend(warnings)
        result = sorted(schools.values(), key=lambda school: (BOROUGH_ORDER.get(school['borough'], len(BOROUGH_ORDER)), school['dbn'], school['schoolYear']))
        if directory:
            years_by_dbn = {}
            for school in result:
                years_by_dbn.setdefault(school['dbn'], []).append(school)
            latest_by_dbn = {}
            for dbn, school_years in years_by_dbn.items():
                comparable_years = [school for school in school_years if len(school['evidence']) >= 2]
                selected = max(comparable_years or school_years, key=lambda school: int(school['schoolYear']))
                latest_by_dbn[dbn] = {**selected, 'comparisonAvailable': bool(comparable_years)}
            result = sorted(latest_by_dbn.values(), key=lambda school: (BOROUGH_ORDER.get(school['borough'], len(BOROUGH_ORDER)), school['dbn']))
            if signal == 'gap':
                result = [school for school in result if school['signals']]
            elif signal == 'missing':
                result = [school for school in result if not school['signals']]
            if gap_threshold:
                result = [school for school in result if any(e.get('gap', 0) >= gap_threshold and (e.get('denominator') or 0) >= 10 and (e.get('graduation') or {}).get('denominator', 0) >= 10 for e in school.get('evidence', []))]
            total = len(result)
            if cursor:
                try: result = result[result.index(next(school for school in result if f"{school['borough']}|{school['dbn']}" == cursor)) + 1:]
                except StopIteration: result = []
            page = result[:limit]
            next_cursor = f"{page[-1]['borough']}|{page[-1]['dbn']}" if len(result) > limit else None
            return {'statusCode': 200, 'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'schools': page, 'total': total, 'nextCursor': next_cursor, 'hasMore': next_cursor is not None})}
        if signal == 'gap':
            result = [school for school in result if school['signals']]
        elif signal == 'missing':
            result = [school for school in result if not school['signals']]
        if gap_threshold:
            result = [school for school in result if any(e.get('gap', 0) >= gap_threshold and (e.get('denominator') or 0) >= 10 and (e.get('graduation') or {}).get('denominator', 0) >= 10 for e in school.get('evidence', []))]
        total = len(result)
        if cursor:
            try: result = result[result.index(next(school for school in result if f"{school['borough']}|{school['dbn']}|{school['schoolYear']}" == cursor)) + 1:]
            except StopIteration: result = []
        page = result[:limit]
        next_cursor = f"{page[-1]['borough']}|{page[-1]['dbn']}|{page[-1]['schoolYear']}" if len(result) > limit else None
        return {'statusCode': 200, 'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'schools': page, 'total': total, 'nextCursor': next_cursor, 'hasMore': next_cursor is not None})}
    except Exception as error:
        return {'statusCode': 502, 'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': str(error)})}


class handler(BaseHTTPRequestHandler):
    """Vercel Python runtime adapter for the portfolio endpoint."""

    def _respond(self, result):
        body = result['body'].encode('utf-8')
        self.send_response(result['statusCode'])
        for name, value in result.get('headers', {}).items():
            self.send_header(name, value)
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)

    def do_GET(self):
        query = {key: values[-1] for key, values in urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).items()}
        self._respond(portfolio_response(type('Request', (), {'args': query})()))

    def do_OPTIONS(self):
        self._respond({'statusCode': 204, 'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}, 'body': ''})
