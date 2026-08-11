#!/usr/bin/env python3
"""Fetch and normalize the relevant NYC records into a reproducible snapshot."""
import json
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from src.data.normalize import API_URL, audit_rows

where = "school_type='High School' AND (metric_display_name like '4-Year Graduation Rate%' OR metric_display_name like 'Percentage of Students with 90%+ Attendance%')"
rows, offset, page_size = [], 0, 50000
while True:
    params = urllib.parse.urlencode({'$limit': page_size, '$offset': offset, '$where': where})
    with urllib.request.urlopen(f'{API_URL}?{params}', timeout=60) as response:
        page = json.load(response)
    rows.extend(page)
    if len(page) < page_size:
        break
    offset += page_size

result = audit_rows(rows)
payload = {'source': API_URL, 'fetchedOn': date.today().isoformat(), 'records': result['pairs']}
output = Path(__file__).parents[1] / 'data' / 'portfolio-snapshot.json'
output.parent.mkdir(exist_ok=True)
output.write_text(json.dumps(payload, separators=(',', ':')) + '\n')
print(f'Wrote {len(result["pairs"])} school-demographic pairs to {output}')
