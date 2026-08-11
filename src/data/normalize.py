API_URL = 'https://data.cityofnewyork.us/resource/dnpx-dfnc.json'

DEMOGRAPHICS = {
    'female': 'Female', 'male': 'Male', 'neither female nor male': 'Neither Female nor Male',
    'black': 'Black', 'white': 'White', 'asian': 'Asian', 'hispanic': 'Hispanic',
    'hispanic or latinx': 'Hispanic', 'multiracial': 'Multiracial',
    'native american': 'Native American', 'native american or american indian': 'Native American',
    'native hawaiian or pacific islander': 'Native Hawaiian or Pacific Islander',
}


def borough_from_dbn(dbn=''):
    return {'M': 'Manhattan', 'X': 'Bronx', 'K': 'Brooklyn', 'Q': 'Queens', 'R': 'Staten Island'}.get(dbn[2:3].upper(), 'Unknown')


def normalize_demographic(value=''):
    return DEMOGRAPHICS.get(value.strip().lower())


def metric_kind(display_name=''):
    name = display_name.lower()
    if '4-year graduation rate' in name:
        return 'graduation4'
    if '90%+ attendance' in name:
        return 'attendance90'
    if '>90% attendance' in name:
        return 'attendance90Strict'
    if 'average student attendance' in name:
        return 'attendanceAverage'
    return None


def normalize_record(row):
    display_name = row.get('metric_display_name', '')
    suffix = ' - '.join(display_name.split(' - ')[1:])
    demographic = normalize_demographic(suffix)
    if demographic is None and (not suffix or suffix.lower() == 'all students'):
        demographic = 'All Students'
    try:
        value = float(row['metric_value']) if row.get('metric_value', '') != '' else None
    except (TypeError, ValueError):
        value = None
    try:
        denominator = int(row['number_of_students']) if row.get('number_of_students', '') != '' else None
    except (TypeError, ValueError):
        denominator = None
    return {
        'dbn': row.get('dbn', '').strip().upper(), 'schoolName': row.get('school_name', '').strip(),
        'schoolYear': str(row.get('school_year', '')), 'reportYear': str(row.get('report_year', '')),
        'schoolType': row.get('school_type', '').strip(), 'reportType': row.get('report_type', '').strip(),
        'borough': borough_from_dbn(row.get('dbn', '')), 'kind': metric_kind(display_name),
        'demographic': demographic, 'value': value, 'denominator': denominator,
        'sourceMetric': display_name, 'sourceVariable': row.get('metric_variable_name', ''),
    }


def is_high_school(record):
    text = f"{record['schoolType']} {record['reportType']}".lower()
    return 'high school' in record['schoolType'].lower() and 'transfer' not in text and 'yabc' not in text


def audit_rows(rows):
    normalized = [normalize_record(row) for row in rows]
    normalized = [row for row in normalized if is_high_school(row) and row['kind'] and row['demographic']]
    groups, warnings = {}, []
    for row in normalized:
        key = f"{row['dbn']}|{row['schoolYear']}|{row['demographic']}|{row['kind']}"
        if key in groups:
            warnings.append({'type': 'duplicate', 'key': key})
        groups[key] = row
        if row['value'] is None:
            warnings.append({'type': 'missing-value', 'key': key})
        if row['denominator'] is not None and row['denominator'] < 10:
            warnings.append({'type': 'small-denominator', 'key': key, 'denominator': row['denominator']})
    pairs = []
    for key, row in groups.items():
        if row['kind'] != 'attendance90':
            continue
        graduation = groups.get(key.replace('|attendance90', '|graduation4'))
        pairs.append({**row, 'graduation': graduation})
        if graduation is None:
            warnings.append({'type': 'unmatched-graduation', 'key': key})
    return {'records': list(groups.values()), 'pairs': pairs, 'warnings': warnings}
