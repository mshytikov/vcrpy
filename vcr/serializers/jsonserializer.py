from vcr.request import Request
from . import compat
try:
    import simplejson as json
except ImportError:
    import json


def _json_default(obj):
    if isinstance(obj, frozenset):
        return dict(obj)
    return obj


def _fix_response_bytes(d):
    d['body']['string'] = d['body']['string'].decode('utf-8')
    return d


def deserialize(cassette_string):
    data = json.loads(cassette_string)
    requests = [Request._from_dict(r['request']) for r in data]
    responses = [compat.convert_body_to_bytes(r['response']) for r in data]
    return requests, responses


def serialize(cassette_dict):
    data = ([{
        'request': request._to_dict(),
        'response': _fix_response_bytes(response),
    } for request, response in zip(
        cassette_dict['requests'],
        cassette_dict['responses']
    )])
    return json.dumps(data, indent=4, default=_json_default)
