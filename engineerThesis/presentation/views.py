from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import Presentation  
from engineerThesis.presentation.forms import PresentationForm

def index(request):
    presentations = Presentation.objects.all()
    ctx = { 'presentations': presentations}
    return render_to_response('presentation/index.html', ctx)

def presentations(request):
    presentations = Presentation.objects.all()
    ctx = { 'presentations': presentations}
    return render_to_response('presentation/presentations.html', ctx)


#todo model form
def add_presentation(request):
    presentations = Presentation.objects.all()
    
    success = False
    title = ""
    description = ""
    
    if request.method == "POST":
        presentation_form = PresentationForm(request.POST)
        
        if presentation_form.is_valid():
            title = presentation_form.cleaned_data['title']
            description = presentation_form.cleaned_data['description']
            
            new_presentation = Presentation()
            new_presentation.title = title
            new_presentation.description = description
            new_presentation.save()

            success = True
    else:
        presentation_form = PresentationForm()
    ctx = { 'presentations': presentations,
           'presentation_form': presentation_form,
           'title': title,
           'description': description,
           'success': success,
    }
    return render_to_response('presentation/add_presentation.html', ctx)