import unittest
from src.data.normalize import audit_rows, borough_from_dbn, normalize_demographic


def row(metric_display_name, metric_value='0.8', number_of_students='50'):
    return {'dbn': '01M292', 'school_name': 'Sample High', 'school_year': '2023', 'report_year': '2024', 'school_type': 'High school', 'report_type': 'HS', 'metric_display_name': metric_display_name, 'metric_value': metric_value, 'number_of_students': number_of_students}


class NormalizeTests(unittest.TestCase):
    def test_borough(self):
        self.assertEqual(borough_from_dbn('01M292'), 'Manhattan')

    def test_demographic_variants(self):
        self.assertEqual(normalize_demographic('Hispanic or Latinx'), 'Hispanic')
        self.assertEqual(normalize_demographic('Native American or American Indian'), 'Native American')

    def test_matches_attendance_and_graduation(self):
        result = audit_rows([row('Percentage of Students with 90%+ Attendance - Female', '0.84'), row('4-Year Graduation Rate - Female', '0.88')])
        self.assertEqual(result['pairs'][0]['graduation']['value'], 0.88)

    def test_flags_quality_warnings(self):
        result = audit_rows([row('Percentage of Students with 90%+ Attendance - Male', number_of_students='5'), row('Percentage of Students with 90%+ Attendance - Male', number_of_students='5')])
        warning_types = {warning['type'] for warning in result['warnings']}
        self.assertTrue({'duplicate', 'small-denominator', 'unmatched-graduation'} <= warning_types)

    def test_excludes_non_high_school(self):
        middle = row('4-Year Graduation Rate - Female')
        middle['school_type'] = 'Middle school'
        self.assertEqual(len(audit_rows([middle])['records']), 0)


if __name__ == '__main__':
    unittest.main()
