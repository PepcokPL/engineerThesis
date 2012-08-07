from django import forms
from engineerThesis.presentation.models import Slide, Position

class PresentationForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    
class SlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        exclude = ('presentation', 'created_at', 'order_number',)
    
class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        exclude = ('id',)