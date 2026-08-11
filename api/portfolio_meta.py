"""Fast, cache-independent metadata for Portfolio Review filters."""
import json
from http.server import BaseHTTPRequestHandler


def metadata_response(request=None):
    body = json.dumps({'years': [str(year) for year in range(2015, 2023)], 'boroughs': ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island'], 'signals': ['all', 'gap', 'missing']})
    return {'statusCode': 200, 'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}, 'body': body}


class handler(BaseHTTPRequestHandler):
    """Vercel Python runtime adapter for the metadata endpoint."""

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
        self._respond(metadata_response())

    def do_OPTIONS(self):
        self._respond({'statusCode': 204, 'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'}, 'body': ''})
