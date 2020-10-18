import re

BRACKET_PARAM = re.compile(r'(\w+)\[(\w+)\]')


def parse_querystring(request):
    params = {}
    for key, value in request.args.items(multi=True):
        matches = BRACKET_PARAM.match(key)
        if matches:
            key = matches.group(1)
            params.setdefault(key, {})
            params[key].update({matches.group(2): value})
        else:
            params[key] = value
    return params
