#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
import json
from api.portfolio import portfolio_response
from api.portfolio_meta import metadata_response


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ('/api/portfolio', '/api/portfolio/meta', '/api/portfolio_meta'):
            request = type('Request', (), {'args': {key: values[-1] for key, values in parse_qs(parsed.query).items()}})()
            metadata_path = parsed.path in ('/api/portfolio/meta', '/api/portfolio_meta')
            result = metadata_response(request) if metadata_path else portfolio_response(request)
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
