from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('%s.olde.views' % settings.MODULE,
    url(r'^json/view/$', 'json_view', name='json-view'),
    url(r'^json/view/all$', 'json_view_all', name='json-view-all'),
    url(r'^view/$', 'view', name='view'),
    url(r'^$', 'index', name='index'),
)
