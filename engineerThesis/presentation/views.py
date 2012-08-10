from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from models import Presentation, Slide
from engineerThesis.presentation.forms import PresentationForm, PositionForm,\
    SlideForm
from engineerThesis.presentation.models import Position

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

def presentation_details(request, presentation_id):
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    p_slides = Slide.objects.filter(presentation=presentation_id)
    ctx = { 'presentation': presentation,
           'slides': p_slides,
    }
    return render_to_response('presentation/presentation_details.html', ctx)

def add_slide(request, presentation_id, slide_id=None):
    
    if slide_id: 
        slide =  get_object_or_404(Slide, pk=slide_id)
        position = get_object_or_404(Position, pk=slide_id)
        
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    success = False
    
    if request.method == "POST":
        slide_form = SlideForm(request.POST)
        position_form = PositionForm(request.POST)
        if slide_form.is_valid() and position_form.is_valid():
            s_form = SlideForm(request.POST)
            new_slide = s_form.save(commit=False)
            new_slide.presentation = presentation
            new_slide.order_number = presentation.get_max_slide_order_number()
            new_slide.save()
            
            p_form = PositionForm(request.POST)
            new_position = p_form.save(commit=False)
            new_position.id = new_slide
            new_position.save()
            
            success = True
    
    slide_form = SlideForm(instance=slide)
    position_form = PositionForm(instance=position)
    
    ctx = {
           'slide_form': slide_form,
           'position_form': position_form,
           'presentation_id': presentation.id,
           'success': success,
    }
    
    return render_to_response('presentation/add_slide.html', ctx)