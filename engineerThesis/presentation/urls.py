from django.conf.urls.defaults import *

urlpatterns = patterns('engineerThesis.presentation.views',
    url(r'^$', 'index', name='presentation_index'),
    url(r'^presentations/$', 'presentations', name='presentation_presentations'),   
    url(r'^add_presentation/$', 'add_presentation', name='presentation_add_presentation'),
    url(r'^(?P<presentation_id>\d+)/details/$', 'presentation_details', name='presentation_details'),
    url(r'^presentation_edit/(?P<presentation_id>\d+)/$', 'edit_presentation', name='presentation_edit'),
    url(r'^presentation_delete/(?P<presentation_id>\d+)/$', 'delete_presentation', name='presentation_delete'),
    url(r'^presentation_preview/(?P<presentation_id>\d+)/$', 'presentation_preview', name='presentation_preview'),
    url(r'^presentation_download/(?P<presentation_id>\d+)/$', 'presentation_download', name='presentation_download'),
    
    url(r'^(?P<presentation_id>\d+)/add_slide/$', 'add_slide', name='add_slide'),
    url(r'^(?P<presentation_id>\d+)/edit_slide/(?P<slide_id>\d+)/$', 'edit_slide', name='edit_slide'),
    url(r'^(?P<presentation_id>\d+)/delete_slide/(?P<slide_id>\d+)/$', 'delete_slide', name='delete_slide'),
    url(r'^(?P<presentation_id>\d+)/preview_slide/(?P<slide_id>\d+)/$', 'preview_slide', name='preview_slide'),
    url(r'^generate_slide_preview/(?P<slide_id>\d+)/$', 'generate_slide_preview', name='generate_slide_preview'), 
    
)