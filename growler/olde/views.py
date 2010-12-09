from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from crew.metrics.httpapi import HttpAPI
from datetime import datetime
import json


def index(request):
    return render_to_response('olde/index.html',
        context_instance=RequestContext(request))


def view(request):
    return render_to_response('olde/view.html',
        context_instance=RequestContext(request))


def json_view(request):
    if not request.method == 'POST':
        return HttpResponse('')
    # Parse query.
    ns = request.POST['ns']
    start = float(request.POST['start'])
    end = float(request.POST['end'])
    interval = 1 # TODO
    # Retrieve data.
    api = HttpAPI(namespace=ns, apikey='test', url=settings.FLAMONGO_ENDPOINT)
    ret = api.retrieve(start_time=start, end_time=end, interval=interval)
    # XXX Begin hack
    acc = {}
    for x in ret:
        try:
            acc[x['timestamp']].append(x)
        except KeyError:
            acc[x['timestamp']] = [x]
    y = []
    for k, values in acc.items():
        count = len(values)
        y.append({'timestamp': k, 'count': count})
    # XXX End hack
    # return as JSON.
    return HttpResponse(json.dumps(y), mimetype='text/json')
