from django.conf.urls.defaults import *

urlpatterns = patterns('engineerThesis.presentation.views',
    url(r'^$', 'index', name='presentation_index'),
    url(r'^presentations/$', 'presentations', name='presentation_presentations'),   
    url(r'^add_presentation/$', 'add_presentation', name='presentation_add_presentation'),                
    
)