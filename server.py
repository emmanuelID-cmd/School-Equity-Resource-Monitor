#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
import json
import os
from api.portfolio import portfolio_response
from api.portfolio_meta import metadata_response
from api.profile import profile_response
from api.budget import budget_response, budget_search_response


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
    supabase_url = os.environ.get('SUPABASE_URL') or values.get('SUPABASE_URL', '')
    publishable_key = os.environ.get('SUPABASE_PUBLISHABLE_KEY') or values.get('SUPABASE_PUBLISHABLE_KEY', '')
    return {'supabaseUrl': supabase_url, 'publishableKey': publishable_key}


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
        if parsed.path in ('/api/portfolio', '/api/portfolio/meta', '/api/portfolio_meta', '/api/profile', '/api/budget', '/api/budget/search'):
            request = type('Request', (), {'args': {key: values[-1] for key, values in parse_qs(parsed.query).items()}})()
            metadata_path = parsed.path in ('/api/portfolio/meta', '/api/portfolio_meta')
            result = metadata_response(request) if metadata_path else (profile_response(request) if parsed.path == '/api/profile' else budget_search_response(request) if parsed.path == '/api/budget/search' else budget_response(request) if parsed.path == '/api/budget' else portfolio_response(request))
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
    port = int(os.environ.get('PORT', '4173'))
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()
