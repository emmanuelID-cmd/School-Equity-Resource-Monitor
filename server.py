#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
import json
from api.portfolio import portfolio_response
from api.portfolio_meta import metadata_response
from api.profile import profile_response


def public_config():
    values = {}
    try:
        with open('.env', encoding='utf-8') as env_file:
            for line in env_file:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                values[key.strip()] = value.strip().strip('"').strip("'")
    except OSError:
        pass
    return {'supabaseUrl': values.get('SUPABASE_URL', ''), 'publishableKey': values.get('SUPABASE_PUBLISHABLE_KEY', '')}


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/config':
            body = json.dumps(public_config()).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if parsed.path in ('/api/portfolio', '/api/portfolio/meta', '/api/portfolio_meta', '/api/profile'):
            request = type('Request', (), {'args': {key: values[-1] for key, values in parse_qs(parsed.query).items()}})()
            metadata_path = parsed.path in ('/api/portfolio/meta', '/api/portfolio_meta')
            result = metadata_response(request) if metadata_path else (profile_response(request) if parsed.path == '/api/profile' else portfolio_response(request))
            body = result['body'].encode()
            self.send_response(result['statusCode'])
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


if __name__ == '__main__':
    ThreadingHTTPServer(('127.0.0.1', 4173), Handler).serve_forever()
