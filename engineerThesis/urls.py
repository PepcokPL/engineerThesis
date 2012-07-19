from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('presentation.urls')),
    (r'^admin/', include(admin.site.urls)),
                       
                       
)

urlpatterns += patterns('presnetation.views',
    url(r'^presentation/',include ('presentation.urls')),                    
)