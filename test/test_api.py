import json
import unittest
from api import portfolio
from api import portfolio_meta
from api import profile


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
        response = portfolio.portfolio_response(Request(args))
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

    def test_metadata_response_has_filter_options(self):
        response = portfolio_meta.metadata_response(Request({}))
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['years'][0], '2015')
        self.assertEqual(body['years'][-1], '2022')
        self.assertIn('Bronx', body['boroughs'])

    def test_profile_lookup_returns_demographics(self):
        profile._load_pairs = lambda: portfolio._cache
        response = profile.profile_response(Request({'dbn': '01M001', 'school_year': '2024'}))
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['dbn'], '01M001')
        self.assertIn('Female', {row['demographic'] for row in body['demographics']})

    def test_profile_requires_dbn_and_year(self):
        response = profile.profile_response(Request({'dbn': '01M001'}))
        self.assertEqual(response['statusCode'], 400)

    def test_profile_not_found(self):
        profile._load_pairs = lambda: portfolio._cache
        response = profile.profile_response(Request({'dbn': '99Z999', 'school_year': '2024'}))
        self.assertEqual(response['statusCode'], 404)

    def test_profile_includes_unavailable_canonical_demographics(self):
        profile._load_pairs = lambda: portfolio._cache
        response = profile.profile_response(Request({'dbn': '01M001', 'school_year': '2024'}))
        body = json.loads(response['body'])
        demographics = {row['demographic']: row for row in body['demographics']}
        self.assertIn('Female', demographics)
        self.assertIn('Male', demographics)
        self.assertIsNone(demographics['Male']['attendance90'])
        self.assertTrue(any('Male demographic record unavailable' in warning for warning in body['warnings']))

    def test_dbn_and_school_name_filters(self):
        _, body = self.call({'dbn': '01M001'})
        self.assertEqual(body['schools'][0]['dbn'], '01M001')
        _, body = self.call({'school_name': 'Other'})
        self.assertEqual(body['schools'][0]['schoolName'], 'Other')


if __name__ == '__main__': unittest.main()
