from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('%s.olde.views' % settings.MODULE,
    url(r'^json/view/$', 'json_view', name='json-view'),
    url(r'^json/view/windows$', 'json_view_windows', name='json-view-windows'),

    url(r'^json/windows/$', 'json_windows_machines',
        name='json-windows-machines'),
    url(r'^json/linux/$', 'json_linux_machines',
        name='json-linux-machines'),
    
		url(r'^json/windows/data/$', 'json_windows_machines_data',
        name='json-windows-machines-data'),
		url(r'^json/linux/data/$', 'json_linux_machines_data',
        name='json-linux-machines-data'),
		url(r'^json/linux/data/both$', 'json_linux_machines_data_both',
        name='json-linux-machines-data-both'),

    url(r'^json/linux-local/data/$', 'json_linux_local_data',
        name='json-linux-local-data'),

    url(r'^json/view/all$', 'json_view_all', name='json-view-all'),

    url(r'^linux/$', 'linux', name='linux'),
    url(r'^windows/$', 'windows', name='windows'),
    url(r'^lab102/full/$', 'view_full', name='view-full'),
    url(r'^lab102/$', 'view', name='view'),

    url(r'^map/windows/$', 'map_windows',
        name='map-windows'),
    url(r'^map/linux/$', 'map_linux',
        name='map-linux'),
    url(r'^map/lab102/$', 'map_lab102',
        name='map-lab102'),

    url(r'^kml/linux/current/$', 'kml_linux_current',
        name='kml-linux-current'),
    url(r'^kml/linux/current/dynamic/$', 'kml_linux_current_dynamic',
        name='kml-linux-current-dynamic'),

    url(r'^kml/lab102/current/$', 'kml_lab102_current',
        name='kml-lab102-current'),
    url(r'^kml/lab102/current/dynamic/$', 'kml_lab102_current_dynamic',
        name='kml-lab102-current-dynamic'),

    url(r'^kml/windows/current/$', 'kml_windows_current',
        name='kml-windows-current'),
    url(r'^kml/windows/current/dynamic/$', 'kml_windows_current_dynamic',
        name='kml-windows-current-dynamic'),
    url(r'^kml/windows/hist/$', 'kml_windows_historical',
        name='kml-windows-historical'),

    url(r'^$', 'index', name='index'),

    url(r'.*', 'error', name='error-404'),
    url(r'404', 'error', name='error-404'),
    url(r'500', 'error500', name='error-500'),
)
