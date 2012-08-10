from django import forms
from engineerThesis.presentation.models import Slide, Position
from tinymce.widgets import TinyMCE

class PresentationForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    
class SlideForm(forms.ModelForm):
    
    content = forms.CharField(widget=TinyMCE(
                                             attrs={'cols': 60, 'rows': 15},
                                             mce_attrs= {'theme': 'advanced'}
                                             ))
    
    class Meta:
        model = Slide
        exclude = ('presentation', 'created_at', 'order_number',)
    
class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        exclude = ('id',)