from django import forms

class PresentationForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    