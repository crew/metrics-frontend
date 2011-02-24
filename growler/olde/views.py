from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from crew.metrics.httpapi import HttpAPI
from datetime import datetime
from random import random
from decorators import default_json_get
import json
import sys
sys.path.append('/net/ccs/lib/python/')
import ccs.hostbase


def index(request):
    return render_to_response('olde/index.html',
        context_instance=RequestContext(request))


def view(request):
    return render_to_response('olde/view.html',
        context_instance=RequestContext(request))

def windows(request):
    return render_to_response('olde/windows.html',
        context_instance=RequestContext(request))

def get_windows_machines():
    hb = ccs.hostbase.HostBase()
    for r in hb.GetRecords():
        if r['room'] == '102' and 'window' in r['os'].lower():
            yield r['hostname'].split('.')[0]

def json_windows_machines(request):
    if not request.method == 'GET':
        return HttpResponse('');
    return HttpResponse(json.dumps(list(get_windows_machines())), mimetype='text/json')

@default_json_get
def json_windows_machines_data(request, ns, start, end):
    interval = 1 # TODO
    # Retrieve data.
    api = HttpAPI(namespace=ns, apikey='test', url=settings.FLAMONGO_ENDPOINT)
    ret = api.retrieve(start_time=start, end_time=end, interval=interval)

    output = {'machines': list(get_windows_machines()), 'data': ret}
    return HttpResponse(json.dumps(output), mimetype='text/json')

@default_json_get
def json_view_all(request, ns, start, end):
    interval = 1 # TODO
    # Retrieve data.
    api = HttpAPI(namespace=ns, apikey='test', url=settings.FLAMONGO_ENDPOINT)
    ret = api.retrieve(start_time=start, end_time=end, interval=interval)
    return HttpResponse(json.dumps(ret), mimetype='text/json')

@default_json_get
def json_view(request, ns, start, end):
    interval = 1 # TODO
    # Retrieve data.
    api = HttpAPI(namespace="windows", apikey='test', url=settings.FLAMONGO_ENDPOINT)
    ret = api.retrieve(start_time=start, end_time=end, interval=interval)
    # XXX Begin hack
    acc = {}
    for x in ret:
        #print x
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
