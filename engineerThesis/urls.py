from django.conf.urls import patterns, include, url
from engineerThesis import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from filebrowser.sites import site

admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('presentation.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^admin/filebrowser/', include(site.urls)),
                       
)

urlpatterns += patterns('presnetation.views',
    url(r'^presentation/',include ('presentation.urls')),                    
)

