from django.conf.urls import patterns, include, url
from engineerThesis import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('presentation.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^staticfiles/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT, 'show_indexes': True}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    (r'^tinymce/', include('tinymce.urls')),
    url(r'', include('multiuploader.urls')),
                       
)

urlpatterns += patterns('presnetation.views',
    url(r'^presentation/',include ('presentation.urls')),                    
)

