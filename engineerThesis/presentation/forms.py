from django import forms
from engineerThesis.presentation.models import Slide, Position, Presentation
from tinymce.widgets import TinyMCE

class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
    
class SlideForm(forms.ModelForm):
    
    content = forms.CharField(widget=TinyMCE(
                                             attrs={'cols': 100, 'rows': 40},
                                             mce_attrs= {
                                                         'theme_advanced_toolbar_location': 'top',
                                                         'plugins': 'advimage,media',
                                                         'file_browser_callback' : 'Presentations.presentationFileBrowser',

                                                        }
                                             ))
    
    class Meta:
        model = Slide
        exclude = ('presentation', 'created_at', 'order_number',)
    
class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        exclude = ('id',)