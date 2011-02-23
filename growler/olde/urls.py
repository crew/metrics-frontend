from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('%s.olde.views' % settings.MODULE,
    url(r'^json/view/$', 'json_view', name='json-view'),
    url(r'^json/windows/$', 'json_windows_machines', name='json-windows-machines'),
    url(r'^json/windows/data/$', 'json_windows_machines_data', name='json-windows-machines-data'),
    url(r'^json/view/all$', 'json_view_all', name='json-view-all'),
    url(r'^windows/$', 'windows', name='windows'),
    url(r'^view/$', 'view', name='view'),
    url(r'^$', 'index', name='index'),
)
