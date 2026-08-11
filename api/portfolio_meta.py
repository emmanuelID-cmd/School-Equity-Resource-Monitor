"""Fast, cache-independent metadata for Portfolio Review filters."""
import json


def handler(request):
    body = json.dumps({'years': [str(year) for year in range(2015, 2023)], 'boroughs': ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island'], 'signals': ['all', 'gap', 'missing']})
    return {'statusCode': 200, 'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}, 'body': body}
