from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from crew.metrics.httpapi import HttpAPI
import time
from datetime import datetime
from pytz import timezone
from random import random
from decorators import default_json_get
import json
import sys
sys.path.append('/net/ccs/lib/python/')
import ccs.hostbase
from django.core.urlresolvers import resolve
from kmlgen import KML

winmachines = [{"point":{"name":"charmander","latitude":"42.33860107","floor":1,"longitude":"-71.09239842"}},{"point":{"name":"charmeleon","latitude":"42.33860937","floor":1,"longitude":"-71.0923954"}},{"point":{"name":"metapod","latitude":"42.3386173","floor":1,"longitude":"-71.09239205"}},{"point":{"name":"charizard","latitude":"42.33862436","floor":1,"longitude":"-71.09238869"}},{"point":{"name":"squirtle","latitude":"42.33863304","floor":1,"longitude":"-71.09238585"}},{"point":{"name":"wartortle","latitude":"42.33864059","floor":1,"longitude":"-71.09238249"}},{"point":{"name":"blastoise","latitude":"42.33864865","floor":1,"longitude":"-71.09237947"}},{"point":{"name":"sandshrew","latitude":"42.33865646","floor":1,"longitude":"-71.09237646"}},{"point":{"name":"nidoran","latitude":"42.33859958","floor":1,"longitude":"-71.0923892"}},{"point":{"name":"nidorina","latitude":"42.33860739","floor":1,"longitude":"-71.09238652"}},{"point":{"name":"weedle","latitude":"42.33861519","floor":1,"longitude":"-71.09238316"}},{"point":{"name":"butterfree","latitude":"42.33862275","floor":1,"longitude":"-71.09237998"}},{"point":{"name":"bulbasaur","latitude":"42.3386308","floor":1,"longitude":"-71.09237679"}},{"point":{"name":"ivysaur","latitude":"42.33863898","floor":1,"longitude":"-71.09237361"}},{"point":{"name":"venusaur","latitude":"42.33864654","floor":1,"longitude":"-71.09237076"}},{"point":{"name":"sandslash","latitude":"42.33865497","floor":1,"longitude":"-71.09236707"}},{"point":{"name":"nidoqueen","latitude":"42.33859214","floor":1,"longitude":"-71.09235684"}},{"point":{"name":"nidorino","latitude":"42.3386002","floor":1,"longitude":"-71.09235383"}},{"point":{"name":"nidoking","latitude":"42.33860776","floor":1,"longitude":"-71.09235047"}},{"point":{"name":"clefairy","latitude":"42.33861618","floor":1,"longitude":"-71.09234712"}},{"point":{"name":"vulpix","latitude":"42.33862387","floor":1,"longitude":"-71.09234394"}},{"point":{"name":"pikachu","latitude":"42.33863204","floor":1,"longitude":"-71.09234075"}},{"point":{"name":"fearow","latitude":"42.33863923","floor":1,"longitude":"-71.09233757"}},{"point":{"name":"spearow","latitude":"42.33864691","floor":1,"longitude":"-71.09233472"}},{"point":{"name":"raticate","latitude":"42.33859103","floor":1,"longitude":"-71.09226448"}},{"point":{"name":"rattata","latitude":"42.33858434","floor":1,"longitude":"-71.09225978"}},{"point":{"name":"pidgeot","latitude":"42.33857715","floor":1,"longitude":"-71.09225458"}},{"point":{"name":"pidgeotto","latitude":"42.33856934","floor":1,"longitude":"-71.09224888"}},{"point":{"name":"caterpie","latitude":"42.33858805","floor":1,"longitude":"-71.09227286"}},{"point":{"name":"kakuna","latitude":"42.33858112","floor":1,"longitude":"-71.09226766"}},{"point":{"name":"beedrill","latitude":"42.3385738","floor":1,"longitude":"-71.09226246"}},{"point":{"name":"pidgey","latitude":"42.33856637","floor":1,"longitude":"-71.09225743"}}]

linmachines = [{"point":{"name":"choplifter","latitude":"42.33854258","floor":1,"longitude":"-71.09246933"}},{"point":{"name":"spaceinvaders","latitude":"42.33855038","floor":1,"longitude":"-71.09246665"}},{"point":{"name":"blueprint","latitude":"42.33855819","floor":1,"longitude":"-71.09246329"}},{"point":{"name":"bumpnjump","latitude":"42.33856625","floor":1,"longitude":"-71.09246028"}},{"point":{"name":"attackufo","latitude":"42.33858409","floor":1,"longitude":"-71.09245089"}},{"point":{"name":"alienarena","latitude":"42.33859177","floor":1,"longitude":"-71.09244787"}},{"point":{"name":"orbit","latitude":"42.33859983","floor":1,"longitude":"-71.09244469"}},{"point":{"name":"seawolf","latitude":"42.33860739","floor":1,"longitude":"-71.09244133"}},{"point":{"name":"computerspace","latitude":"42.33861556","floor":1,"longitude":"-71.09243798"}},{"point":{"name":"startrek","latitude":"42.33862325","floor":1,"longitude":"-71.09243513"}},{"point":{"name":"mrdo","latitude":"42.3386313","floor":1,"longitude":"-71.09243178"}},{"point":{"name":"millipede","latitude":"42.33863898","floor":1,"longitude":"-71.09242859"}},{"point":{"name":"spyhunter","latitude":"42.33858211","floor":1,"longitude":"-71.092442"}},{"point":{"name":"hattrick","latitude":"42.33858979","floor":1,"longitude":"-71.09243865"}},{"point":{"name":"avenger","latitude":"42.33859772","floor":1,"longitude":"-71.09243547"}},{"point":{"name":"agentx","latitude":"42.33860553","floor":1,"longitude":"-71.09243262"}},{"point":{"name":"brix","latitude":"42.3386137","floor":1,"longitude":"-71.09242943"}},{"point":{"name":"berzerk","latitude":"42.33862176","floor":1,"longitude":"-71.09242641"}},{"point":{"name":"mousetrap","latitude":"42.33862919","floor":1,"longitude":"-71.09242306"}},{"point":{"name":"upscope","latitude":"42.33863762","floor":1,"longitude":"-71.09241937"}},{"point":{"name":"turtles","latitude":"42.33859041","floor":1,"longitude":"-71.09234796"}},{"point":{"name":"armorattack","latitude":"42.33859809","floor":1,"longitude":"-71.09234477"}},{"point":{"name":"warlords","latitude":"42.33860615","floor":1,"longitude":"-71.09234176"}},{"point":{"name":"missilecommand","latitude":"42.33861445","floor":1,"longitude":"-71.09233857"}},{"point":{"name":"joust","latitude":"42.33862213","floor":1,"longitude":"-71.09233555"}},{"point":{"name":"biplane","latitude":"42.33862981","floor":1,"longitude":"-71.09233203"}},{"point":{"name":"timepilot","latitude":"42.33863774","floor":1,"longitude":"-71.09232885"}},{"point":{"name":"gyruss","latitude":"42.33864555","floor":1,"longitude":"-71.09232566"}},{"point":{"name":"majorhavoc","latitude":"42.33858273","floor":1,"longitude":"-71.09231544"}},{"point":{"name":"alleyrally","latitude":"42.33859078","floor":1,"longitude":"-71.09231208"}},{"point":{"name":"skydiver","latitude":"42.33859846","floor":1,"longitude":"-71.0923089"}},{"point":{"name":"bubbles","latitude":"42.33860652","floor":1,"longitude":"-71.09230555"}},{"point":{"name":"batterup","latitude":"42.3386142","floor":1,"longitude":"-71.09230236"}},{"point":{"name":"tank","latitude":"42.33862213","floor":1,"longitude":"-71.09229968"}},{"point":{"name":"apollo14","latitude":"42.33863019","floor":1,"longitude":"-71.09229633"}},{"point":{"name":"jumpbug","latitude":"42.33863737","floor":1,"longitude":"-71.09229331"}},{"point":{"name":"breakout","latitude":"42.33858112","floor":1,"longitude":"-71.09230605"}},{"point":{"name":"blackwidow","latitude":"42.33858892","floor":1,"longitude":"-71.0923032"}},{"point":{"name":"hiway","latitude":"42.33859673","floor":1,"longitude":"-71.09230018"}},{"point":{"name":"bosconian","latitude":"42.33860503","floor":1,"longitude":"-71.09229683"}},{"point":{"name":"astroblaster","latitude":"42.33861271","floor":1,"longitude":"-71.09229381"}},{"point":{"name":"eagle","latitude":"42.33862015","floor":1,"longitude":"-71.09229046"}},{"point":{"name":"gauntlet","latitude":"42.3386282","floor":1,"longitude":"-71.09228761"}},{"point":{"name":"vanguard","latitude":"42.33863576","floor":1,"longitude":"-71.09228442"}}]

def index(request):
    return render_to_response('olde/index.html',
        context_instance=RequestContext(request))

def view(request):
    return render_to_response('olde/view.html',
        context_instance=RequestContext(request))

def windows(request):
    return render_to_response('olde/windows.html',
        context_instance=RequestContext(request))

def linux(request):
    return render_to_response('olde/linux.html',
        context_instance=RequestContext(request))

def get_windows_machines():
    hb = ccs.hostbase.HostBase()
    for r in hb.GetRecords():
        if r['room'] == '102' and 'window' in r['os'].lower():
            yield r['hostname'].split('.')[0]

def get_linux_machines():
    hb = ccs.hostbase.HostBase()
    for r in hb.GetRecords():
        if r['room'] == '102' and 'ubuntu' in r['os'].lower():
            yield r['hostname'].split('.')[0]

def json_windows_machines(request):
    if not request.method == 'GET':
        return HttpResponse('')
    return HttpResponse(json.dumps(list(get_windows_machines())), mimetype='text/json')

def json_linux_machines(request):
    if not request.method == 'GET':
        return HttpResponse('')
    return HttpResponse(json.dumps(list(get_linux_machines())), mimetype='text/json')

def windows_data(start, end):
    interval = 1 # TODO
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
    return output

def linux_data(start, end, local):
    interval = 600
    api = HttpAPI(namespace='linux', apikey='test', url=settings.FLAMONGO_ENDPOINT)
    s = datetime.utcfromtimestamp(start)
    s = datetime(s.year, s.month, s.day, 0, 0) # Get the start of day.
    s = time.mktime(s.timetuple())
    ret = api.retrieve(start_time=s, end_time=end, interval=interval,
        attributes={'is_local': local})
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
    return output

@default_json_get
def json_windows_machines_data(request, ns, start, end):
    interval = 1 # TODO
    # Retrieve data.
    api = HttpAPI(namespace=ns, apikey='test', url=settings.FLAMONGO_ENDPOINT)
    ret = api.retrieve(start_time=start, end_time=end, interval=interval)

    output = {'machines': list(get_windows_machines()), 'data': ret}
    return HttpResponse(json.dumps(output), mimetype='text/json')

@default_json_get
def json_linux_machines_data(request, ns, start, end):
    interval = 1 # TODO
    # Retrieve data.
    api = HttpAPI(namespace=ns, apikey='test', url=settings.FLAMONGO_ENDPOINT)
    ret = api.retrieve(start_time=start, end_time=end, interval=interval,
        attributes={'is_local': True})

    for r in ret:
        r['hostname'] = r['hostname'].split('.')[0]

    output = {'machines': list(get_linux_machines()), 'data': ret}
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
    if 'window' in ns.lower():
        return json_view_windows(request, ns, start, end)
    elif 'linux' in ns.lower():
        return json_linux_local_data(request)
    else: #'all' in ns.lower():
        output_windows = windows_data(start, end)
        output_linux_local = linux_data(start, end, True)
        output_linux_ssh = linux_data(start, end, False)
        output = { 'linux': { 'local': output_linux_local, 'ssh': output_linux_ssh }
                 , 'windows': output_windows } 
        return HttpResponse(json.dumps(output), mimetype='text/json')

@default_json_get
def json_view_windows(request, ns, start, end):
    # Retrieve data.
    output = windows_data(start, end)
    # return as JSON.
    return HttpResponse(json.dumps(output), mimetype='text/json')

@default_json_get
def json_linux_local_data(request, ns, start, end):
    output = linux_data(start, end)
    return HttpResponse(json.dumps(output), mimetype='text/json')

def kml_windows_current(request):
    return render_to_response('olde/windows-current.kml',{"absurl":"%s://%s" % (request.is_secure() and 'https' or 'http', request.get_host())},
        context_instance=RequestContext(request), mimetype='application/vnd.google-earth.kml+xml')

def kml_linux_current(request):
    return render_to_response('olde/linux-current.kml',{"absurl":"%s://%s" % (request.is_secure() and 'https' or 'http', request.get_host())},
        context_instance=RequestContext(request), mimetype='application/vnd.google-earth.kml+xml')

def kml_lab102_current(request):
    return render_to_response('olde/lab102-current.kml',{"absurl":"%s://%s" % (request.is_secure() and 'https' or 'http', request.get_host())},
        context_instance=RequestContext(request), mimetype='application/vnd.google-earth.kml+xml')

def kml_windows_current_dynamic(request):
    return HttpResponse(kml_from_list('CCIS Windows', get_windows_current()),
                        'application/vnd.google-earth.kml+xml')

def kml_linux_current_dynamic(request):
    return HttpResponse(kml_from_list('CCIS Linux', get_linux_current()),
                        'application/vnd.google-earth.kml+xml')

def kml_lab102_current_dynamic(request):
    return HttpResponse(kml_from_list('CCIS Lab 102',
                                      get_windows_current() + 
                                      get_linux_current()),
                        'application/vnd.google-earth.kml+xml')

def kml_from_list(name, lst):
    k = KML(name, '')
    # XXX hardcoding urls.
    k.add_style("inuse", "http://maps.google.com/mapfiles/ms/icons/red.png")
    k.add_style("unused", "http://maps.google.com/mapfiles/ms/icons/green.png")
    lst.sort(key=lambda r: r['longitude'])
    def get_description(c):
        # date = datetime.fromtimestamp(c['timestamp'],
        #     timezone('US/Eastern')).strftime("%A at %I:%M%p")
        prefix = 'In Use' if c['inuse'] else 'Free'
        date = c['timestamp'].strftime("%A at %I:%M%p")
        return '%s as of %s' % (prefix, date)
    def get_style(c):
        return 'inuse' if c['inuse'] else 'unused'
    for c in lst:
        k.add_placemark(c['hostname'], c['longitude'], c['latitude'],
            altitude=c['floor'], style=get_style(c), desc=get_description(c))
    return k.output_kml()

def get_windows_current():
    api = HttpAPI(namespace='windows', apikey='test',
        url=settings.FLAMONGO_ENDPOINT)
    now = time.time()
    # pad with an extra minute
    then = now - 660
    newlist = []
    for m in winmachines:
        np = m['point']
        ret = api.retrieve_last(attributes={'hostname': np['name']})[0]
        # NOTE: The time below appears to be unreliable.
        # XXX: temporary fix.
        timestamp = datetime.fromtimestamp(ret['timestamp'] - 3600 * 4)
        newlist.append({'hostname': np['name'], 'longitude': np['longitude'],
            'latitude': np['latitude'], 'floor': np['floor'],
            'inuse': (ret['timestamp'] >= then), 'timestamp': timestamp})
    return newlist

def get_linux_current():
    api = HttpAPI(namespace='linux', apikey='test',
        url=settings.FLAMONGO_ENDPOINT)
    newlist = []
    for m in linmachines:
        np = m['point']
        ret = api.retrieve_last(
            attributes={'hostname': '%s.ccs.neu.edu' % np['name'],
                'is_local': True})[0]
        # XXX: temporary fix.
        timestamp = datetime.fromtimestamp(ret['timestamp'] - 3600 * 4)
        newlist.append({'hostname': np['name'], 'longitude': np['longitude'],
            'latitude': np['latitude'], 'floor': np['floor'],
            # last event was a login (so it's in use)
            'inuse': (ret['event'] == 'login'),
            'timestamp': timestamp})
    return newlist

def kml_windows_historical(request):
    return HttpResponse('')

def get_absurl(request):
    if request.is_secure():
        return 'https://%s' % request.get_host()
    return 'http://%s' % request.get_host()

def map_windows(request):
    return render_to_response('olde/windows-map.html',
        {"absurl": get_absurl(request)},
        context_instance=RequestContext(request))

def map_linux(request):
    return render_to_response('olde/linux-map.html',
        {"absurl": get_absurl(request)},
        context_instance=RequestContext(request))

def map_lab102(request):
    return render_to_response('olde/lab102-map.html',
        {"absurl": get_absurl(request)},
        context_instance=RequestContext(request))
