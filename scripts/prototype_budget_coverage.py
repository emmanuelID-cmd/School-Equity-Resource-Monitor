#!/usr/bin/env python3
"""Read-only coverage matrix for the NYCPS budget-source prototype."""

import argparse
import json

from prototype_budget_source import fetch_report


def run(codes, fiscal_years):
    reports = []
    for code in codes:
        for fiscal_year in fiscal_years:
            try:
                reports.append(fetch_report(code, fiscal_year))
            except Exception as error:  # keep the matrix useful when one request fails
                reports.append({
                    'lookup_code': code,
                    'fiscal_year': f'FY {fiscal_year}',
                    'status': 'request_error',
                    'error': str(error),
                })
    matched = [report for report in reports if report['status'] == 'matched']
    return {
        'schools_tested': len(codes),
        'fiscal_years_tested': fiscal_years,
        'reports_tested': len(reports),
        'reports_matched': len(matched),
        'reports_unavailable': sum(report['status'] == 'unavailable' for report in reports),
        'request_errors': sum(report['status'] == 'request_error' for report in reports),
        'dbn_matches': sum(bool(report.get('dbn')) for report in matched),
        'field_presence': {
            field: sum(bool(report.get(field)) for report in matched)
            for field in ('total_school_funding', 'funding_per_student', 'funding_plus_central_services_per_student')
        },
        'reports': reports,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--school-code', action='append', dest='codes', default=['M425', 'M292', 'X269'], help='Repeat for each four-digit school code')
    parser.add_argument('--fiscal-year', action='append', dest='years', type=int, default=[2024, 2025, 2026], help='Repeat for each fiscal year')
    args = parser.parse_args()
    print(json.dumps(run([code.upper() for code in args.codes], args.years), indent=2))


if __name__ == '__main__':
    main()
