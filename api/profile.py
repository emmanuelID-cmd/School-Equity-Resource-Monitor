"""School Equity Profile API keyed by DBN and school year."""
import json
from http.server import BaseHTTPRequestHandler
from .portfolio import _load_pairs

CANONICAL_DEMOGRAPHICS = ['All Students', 'Asian', 'Black', 'Hispanic', 'Native American', 'Native Hawaiian or Pacific Islander', 'Multiracial', 'White', 'Female', 'Male', 'Neither Female nor Male']


def profile_response(request):
    query = getattr(request, 'args', {}) or {}
    dbn = str(query.get('dbn', '')).strip().upper()
    school_year = str(query.get('school_year', '')).strip()
    if not dbn or not school_year:
        return {'statusCode': 400, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'dbn and school_year are required'})}
    pairs = [p for p in _load_pairs() if p.get('dbn') == dbn and str(p.get('schoolYear')) == school_year]
    if not pairs:
        return {'statusCode': 404, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'School profile not found'})}
    first = pairs[0]
    demographics = []
    warnings = set()
    by_demographic = {pair.get('demographic'): pair for pair in pairs}
    for demographic in CANONICAL_DEMOGRAPHICS:
        pair = by_demographic.get(demographic, {'demographic': demographic, 'value': None, 'denominator': None, 'graduation': None})
        graduation = pair.get('graduation') or {}
        attendance = pair.get('value')
        if attendance is None: warnings.add('Attendance value missing or suppressed')
        if pair.get('denominator') is not None and pair['denominator'] < 10: warnings.add('Attendance denominator below 10')
        if not graduation: warnings.add('Graduation record missing for this school year')
        elif graduation.get('value') is None: warnings.add('Graduation value missing or suppressed')
        elif graduation.get('denominator') is not None and graduation['denominator'] < 10: warnings.add('Graduation denominator below 10')
        if demographic not in by_demographic: warnings.add(f'{demographic} demographic record unavailable for this school year')
        demographics.append({'demographic': demographic, 'attendance90': attendance, 'graduation4': graduation.get('value'), 'attendanceDenominator': pair.get('denominator'), 'graduationDenominator': graduation.get('denominator'), 'gap': abs(graduation['value'] - attendance) if attendance is not None and graduation.get('value') is not None else None})
    body = {'dbn': dbn, 'schoolName': first.get('schoolName'), 'borough': first.get('borough'), 'schoolYear': school_year, 'demographics': demographics, 'matchedRecordCount': sum(1 for item in demographics if item['gap'] is not None), 'warnings': sorted(warnings)}
    return {'statusCode': 200, 'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}, 'body': json.dumps(body)}


class handler(BaseHTTPRequestHandler):
    def _respond(self, result):
        body = result['body'].encode()
        self.send_response(result['statusCode'])
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if self.command != 'HEAD': self.wfile.write(body)

    def do_GET(self):
        from urllib.parse import parse_qs, urlparse
        args = {key: values[-1] for key, values in parse_qs(urlparse(self.path).query).items()}
        result = profile_response(type('Request', (), {'args': args})())
        self._respond(result)

    def do_OPTIONS(self):
        self._respond({'statusCode': 204, 'body': ''})
