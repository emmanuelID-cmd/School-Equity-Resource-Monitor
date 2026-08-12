"""Bounded server-side adapter for the public NYCPS Galaxy Budget Summary."""
import json, re, urllib.parse, urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
import html

GALAXY_URL = 'https://apps.schools.nyc/dsbpo/galaxybudgetsummaryto/default.aspx'
CODE_PATTERN = re.compile(r'^[MXKQR]\d{3}$')

class _Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.hidden = {}; self.parts = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'input' and attrs.get('type') == 'hidden' and attrs.get('name'):
            self.hidden[attrs['name']] = html.unescape(attrs.get('value', ''))
    def handle_data(self, data): self.parts.append(data)

def _valid(code, year):
    code, year = str(code or '').strip().upper(), str(year or '').strip()
    if not CODE_PATTERN.fullmatch(code): return None, 'Use a borough letter (M, X, K, Q, or R) followed by three digits, such as M292.'
    if year not in {str(value) for value in range(2006, 2027)}: return None, 'Choose a fiscal year from 2006 through 2026.'
    return (code, year), None

def _fetch(code, year):
    req = urllib.request.Request(GALAXY_URL, headers={'User-Agent': 'SchoolEquityResourceMonitor/1.0'})
    with urllib.request.urlopen(req, timeout=20) as response: initial = response.read().decode('utf-8', 'replace')
    parser = _Parser(); parser.feed(initial)
    fields = dict(parser.hidden); fields.update({'School_Code': code, 'Fiscal_Year': year, 'Enter': 'Enter'})
    body = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(GALAXY_URL, data=body, headers={'User-Agent': 'SchoolEquityResourceMonitor/1.0', 'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=20) as response: return response.read().decode('utf-8', 'replace')

def budget_response(request):
    query = getattr(request, 'args', {}) or {}; validated, error = _valid(query.get('school_code'), query.get('fiscal_year'))
    if error: return {'statusCode': 400, 'body': json.dumps({'status': 'invalid', 'message': error})}
    code, year = validated
    try: source = _fetch(code, year)
    except TimeoutError: return {'statusCode': 504, 'body': json.dumps({'status': 'timeout', 'message': 'The budget source took too long to respond. Please try again.'})}
    except Exception: return {'statusCode': 502, 'body': json.dumps({'status': 'unavailable', 'message': 'The budget source is temporarily unavailable. Please try again later.'})}
    parser = _Parser(); parser.feed(source); text = re.sub(r'\s+', ' ', ' '.join(parser.parts)).strip()
    if 'Please Enter a  4 Digit School' in text: result = {'status': 'invalid', 'message': 'Galaxy rejected the school code format.'}
    elif 'not found' in text.lower() or 'no record' in text.lower(): result = {'status': 'not_found', 'message': 'No Galaxy budget record was found for this school and fiscal year.'}
    else:
        match = re.search(r'(\d{2}[A-Z]\d{3})\s+-\s+(.+?)(?=\s+\d{2,5}\s|\s+Fiscal Year)', text)
        if not match: result = {'status': 'unavailable', 'message': 'Galaxy returned no recognizable school-level budget record.'}
        else:
            dbn, school_name = match.groups(); source_match = re.search(r'Budget Data Source:\s*(.+?)\s+' + re.escape(dbn), text)
            returned_year = re.search(r'Fiscal Year\s+(20\d{2})\s+Budget Data Source:', text)
            if returned_year and returned_year.group(1) != year:
                result = {'status': 'not_comparable', 'message': f'Galaxy returned fiscal year {returned_year.group(1)} instead of the selected fiscal year {year}. No values were displayed.'}
                return {'statusCode': 502, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(result)}
            records = [{'label': m.group(1).strip(), 'positions': float(m.group(2)), 'budget': int(m.group(3).replace(',', ''))} for m in re.finditer(r'([A-Z][A-Z /&-]{2,60})\s+(\d+\.\d{2})\s+\$\s*([\d,]+)', text)][:100]
            result = {'status': 'partial', 'message': 'Partial budget context. Galaxy budgeted inputs are not definitive actual spending.', 'dbn': dbn, 'schoolCode': code, 'schoolName': school_name.strip(), 'fiscalYear': int(year), 'sourceDate': source_match.group(1).strip() if source_match else None, 'records': records, 'sourceUrl': GALAXY_URL, 'retrievedAt': datetime.now(timezone.utc).isoformat()}
    return {'statusCode': 200 if result['status'] == 'partial' else 404 if result['status'] == 'not_found' else 502, 'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}, 'body': json.dumps(result)}

def budget_search_response(request):
    query = str((getattr(request, 'args', {}) or {}).get('query', '')).strip().upper()
    if not query:
        return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'schools': [], 'total': 0})}
    from .portfolio import _load_pairs
    schools = {}
    for item in _load_pairs():
        dbn = item.get('dbn', '')
        code = dbn[2:] if len(dbn) == 6 else ''
        if query in dbn or query in code or query in item.get('schoolName', '').upper():
            schools[dbn] = {'dbn': dbn, 'schoolCode': code, 'schoolName': item.get('schoolName'), 'borough': item.get('borough')}
    return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'schools': list(schools.values())[:20], 'total': len(schools)})}
