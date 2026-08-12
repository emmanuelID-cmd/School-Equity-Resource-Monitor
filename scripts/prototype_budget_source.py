#!/usr/bin/env python3
"""Read-only prototype for extracting NYCPS School Budget At a Glance fields."""

import argparse
import json
import re
from html import unescape
from urllib.parse import urlencode
from urllib.request import Request, urlopen


BASE_URL = 'https://apps.schools.nyc/dsbpo/sbag/default.aspx'


def text_from_html(document):
    text = unescape(re.sub(r'<[^>]+>', ' ', document))
    return re.sub(r'\s+', ' ', text).strip()


def field(text, label):
    match = re.search(re.escape(label) + r'\s*(\$[\d,]+|N/A|—)', text)
    return match.group(1) if match else None


def fetch_report(school_code, fiscal_year):
    query = urlencode({'DDBSSS_INPUT': school_code, 'fy': fiscal_year})
    request = Request(f'{BASE_URL}?{query}', headers={'User-Agent': 'SchoolEquityResourceMonitor/phase-6.1'})
    with urlopen(request, timeout=20) as response:
        document = response.read().decode('utf-8', errors='replace')
    text = text_from_html(document)
    school_match = re.search(r'School Budget at a Glance School Year\s+([0-9]{4}-[0-9]{2})', text)
    identity_match = re.search(r'\(([0-9]{2}[A-Z][0-9]{3})\)', text)
    return {
        'source': BASE_URL,
        'lookup_code': school_code,
        'fiscal_year': f'FY {fiscal_year}',
        'school_year': school_match.group(1) if school_match else None,
        'dbn': identity_match.group(1) if identity_match else None,
        'total_school_funding': field(text, 'Total School Funding:'),
        'funding_per_student': field(text, 'School Funding per student:'),
        'funding_plus_central_services_per_student': field(text, 'School Funding plus Average Central Services per student:'),
        'status': 'matched' if school_match else 'unavailable',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--school-code', default='M425', help='NYCPS four-digit school code, for example M425')
    parser.add_argument('--fiscal-year', type=int, default=2026, help='Fiscal year number, for example 2026')
    args = parser.parse_args()
    print(json.dumps(fetch_report(args.school_code.upper(), args.fiscal_year), indent=2))


if __name__ == '__main__':
    main()
