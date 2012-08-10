from django.conf.urls.defaults import *

urlpatterns = patterns('engineerThesis.presentation.views',
    url(r'^$', 'index', name='presentation_index'),
    url(r'^presentations/$', 'presentations', name='presentation_presentations'),   
    url(r'^add_presentation/$', 'add_presentation', name='presentation_add_presentation'),
    url(r'^(?P<presentation_id>\d+)/details/$', 'presentation_details', name='presentation_details'),
    url(r'^(?P<presentation_id>\d+)/add_slide/$', 'add_slide', name='add_slide'),
    url(r'^(?P<presentation_id>\d+)/slide_details/(?P<slide_id>\d+)/$', 'add_slide', name='add_slide'),
     
    
)