from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from crew.metrics.httpapi import HttpAPI
import time
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
        try:
            acc[x['timestamp']].append(x)
        except KeyError:
            acc[x['timestamp']] = [x]
    y = []
    for k, values in acc.items():
        count = len(values)
        y.append({'timestamp': k, 'count': count})
    y.sort(key=lambda r: r['timestamp'])
    output = []
    for r in y:
        lastIndex = y.index(r)-1
        if lastIndex >= 0:
            last = y[lastIndex]['timestamp']
            if r['timestamp']-last > 700:
                output.append({'timestamp': r['timestamp']-600, 'count': 0})
                output.append({'timestamp': last+600, 'count': 0})
            output.append(r);
    # XXX End hack
    # return as JSON.
    return HttpResponse(json.dumps(output), mimetype='text/json')

def json_linux_local_data(request):
    ns = 'linux'
    start = float(request.GET['start'])
    end = float(request.GET['end'])
#    interval = int(request.GET['interval'])
    interval = 600
    api = HttpAPI(namespace=ns, apikey='test', url=settings.FLAMONGO_ENDPOINT)
    s = datetime.utcfromtimestamp(start)
    s = datetime(s.year, s.month, s.day, 0, 0) # Get the start of day.
    s = time.mktime(s.timetuple())
    ret = api.retrieve(start_time=s, end_time=end, interval=interval,
        attributes={'is_local': True})
    # Fetch the reboot events.
    reboots = api.retrieve(start_time=s, end_time=end, interval=interval,
        attributes={'event': 'reboot'})
    # Merge then sort the results
    ret = list(ret) + list(reboots)
    ret.sort(key=lambda x: x['timestamp'])
    def get_n(x):
        # The nth interval.
        return int(x - start) // interval
    current_hosts = set()
    current_n = 0
    counts = []
    #
    for record in ret:
        if record['timestamp'] >= start:
            n = get_n(record['timestamp'])
            if n > current_n:
                for i in range(current_n, n):
                    counts.append(len(current_hosts))
                current_n = n
        if record['event'] == 'login':
            current_hosts.add(record['hostname'])
        else:
            if record['hostname'] in current_hosts:
                current_hosts.remove(record['hostname'])
    # Add the tail.
    for i in range(current_n, get_n(end)):
        counts.append(len(current_hosts))
    output = []
    def get_t(start=start, interval=interval):
        # Generate the times.
        x = start
        while True:
            yield start
            start += interval
    for c, ts in zip(counts, get_t()):
        output.append({'timestamp': ts, 'count': c})
    return HttpResponse(json.dumps(output), mimetype='text/json')

#TODO: Write KML Views
def kml_windows_current(request):
    return HttpResponse('')

def kml_windows_historical(request):
    return HttpResponse('')
