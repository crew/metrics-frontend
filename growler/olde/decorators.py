from django.http import HttpResponse
from functools import wraps


def default_json_get(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.method == 'GET':
            # Parse the query.
            ns = request.GET['ns']
            start = float(request.GET['start'])
            end = float(request.GET['end'])
            return f(request, ns, start, end)
        # XXX should return a method not allowed.
        return HttpResponse('')
    return wrapper
