from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.ROOT('media')}, name='media'),

    url(r'^', include('%s.olde.urls' % settings.MODULE, app_name='olde')),
)
