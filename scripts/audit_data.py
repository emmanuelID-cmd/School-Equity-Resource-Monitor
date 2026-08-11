#!/usr/bin/env python3
import json
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from src.data.normalize import API_URL, audit_rows

rows = []
page_size = 50000
offset = 0
where = "school_type='High School' AND (metric_display_name like '4-Year Graduation Rate%' OR metric_display_name like 'Percentage of Students with 90%+ Attendance%')"
while True:
    query = urllib.parse.urlencode({'$limit': page_size, '$offset': offset, '$where': where})
    with urllib.request.urlopen(f'{API_URL}?{query}', timeout=60) as response:
        page = json.load(response)
    rows.extend(page)
    if len(page) < page_size:
        break
    offset += page_size
result = audit_rows(rows)
summary = {
    'fetchedRows': len(rows), 'relevantRecords': len(result['records']),
    'matchedPairs': sum(pair['graduation'] is not None for pair in result['pairs']),
    'unmatchedPairs': sum(pair['graduation'] is None for pair in result['pairs']),
    'warningCounts': dict(Counter(warning['type'] for warning in result['warnings'])),
    'years': sorted({row['schoolYear'] for row in result['records']}),
    'demographics': sorted({row['demographic'] for row in result['records']}),
}
print(json.dumps(summary, indent=2))
