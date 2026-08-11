import json
import unittest
from api import portfolio


class Request:
    def __init__(self, args): self.args = args


class PortfolioApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        portfolio._cache = [
            {'dbn': '01M001', 'schoolYear': '2024', 'schoolName': 'Test', 'borough': 'Manhattan', 'demographic': 'Female', 'value': .60, 'denominator': 20,
             'graduation': {'value': .70, 'denominator': 20}},
            {'dbn': '02M002', 'schoolYear': '2023', 'schoolName': 'Other', 'borough': 'Bronx', 'demographic': 'Male', 'value': .50, 'denominator': 5,
             'graduation': None},
        ]

    def call(self, args):
        response = portfolio.handler(Request(args))
        return response['statusCode'], json.loads(response['body'])

    def test_limit_and_cursor(self):
        status, body = self.call({'limit': '1'})
        self.assertEqual(status, 200); self.assertEqual(len(body['schools']), 1)
        self.assertTrue(body['hasMore'])
        status, next_body = self.call({'limit': '1', 'cursor': body['nextCursor']})
        self.assertEqual(status, 200); self.assertEqual(len(next_body['schools']), 1)

    def test_year_borough_and_gap_filters(self):
        _, body = self.call({'year': '2024', 'borough': 'Manhattan', 'gap': '.15'})
        self.assertEqual(len(body['schools']), 0)
        _, body = self.call({'year': '2024', 'gap': '.05'})
        self.assertEqual(len(body['schools']), 1)

    def test_response_has_warnings(self):
        _, body = self.call({'borough': 'Bronx'})
        self.assertTrue(body['schools'][0]['warnings'])

    def test_invalid_limit_returns_error(self):
        status, body = self.call({'limit': 'not-a-number'})
        self.assertEqual(status, 502); self.assertIn('error', body)


if __name__ == '__main__': unittest.main()
