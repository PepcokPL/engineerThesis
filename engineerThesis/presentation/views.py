from StringIO import StringIO
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse  
from django.shortcuts import render_to_response, get_object_or_404, redirect
from models import Presentation, Slide
from engineerThesis.presentation.forms import PresentationForm, PositionForm,\
    SlideForm
from engineerThesis.presentation.models import Position
from django.template.loader import render_to_string
import re, os
import zipfile
from django.conf import settings
from django.utils import simplejson

#TODO podzial na pliki

def index(request):
    presentations = Presentation.objects.all()
    ctx = { 'presentations': presentations}
    return render_to_response('presentation/index.html', ctx)

def presentations(request):
    presentations = Presentation.objects.all()
    ctx = { 'presentations': presentations}
    return render_to_response('presentation/presentations.html', ctx)


def add_presentation(request, presentation_id=None):
    
    
    if presentation_id:
        presentation = get_object_or_404(Presentation, pk=presentation_id)
    
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
            
    ctx = { 'presentation_form': presentation_form,
           'title': title,
           'description': description,
           'success': success,
    }
    return render_to_response('presentation/add_presentation.html', ctx)

def edit_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    success = False
    edit = True
    
    if request.method == "POST":
        presentation_form = PresentationForm(request.POST)
        if presentation_form.is_valid():
            presentation_form = PresentationForm(request.POST, instance=presentation)
            presentation_form.save()
        success = True
    
    else:
        presentation_form = PresentationForm(instance=presentation)
    
    ctx = {
           'success': success,
           'presentation_form': presentation_form,
           'edit': edit,
    }
    return render_to_response('presentation/add_presentation.html', ctx)   
    
def presentation_details(request, presentation_id):
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    p_slides = Slide.objects.filter(presentation=presentation_id).order_by('order_number')
    ctx = { 'presentation': presentation,
           'slides': p_slides,
    }
    return render_to_response('presentation/presentation_details.html', ctx)

def delete_presentation(request, presentation_id):
    confirmation = False
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    if request.method == "POST" and request.POST['confirm'] == 'Tak':
        presentation.delete()
        confirmation = True
    ctx = {
           'confirmation': confirmation,
           'presentation': presentation,
    }    
    return render_to_response('presentation/delete_presentation.html', ctx)

def presentation_preview(requst, presentation_id):
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    p_slides = Slide.objects.filter(presentation=presentation_id)
    slides_ids = ['generate_slide_preview/'+str(slide.id) for slide in p_slides]
    ctx = {'presentation': presentation,
           'slides_ids': slides_ids,
           'p_slides': p_slides,
           
    }
    return render_to_response('presentation/presentation_preview.html', ctx)

def presentation_download(request, presentation_id):
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    p_slides = Slide.objects.filter(presentation=presentation_id)
    slides_ids = ['generate_slide_preview/'+str(slide.id) for slide in p_slides]
    ctx = {'presentation': presentation,
           'slides_ids': slides_ids,
           'p_slides': p_slides,
           
    }
    
    rednered_template = render_to_string ('presentation/presentation_preview.html', ctx)
    print rednered_template
    fixed_rednered_template = rednered_template.replace('../../../media/uploads', 'media')
    fixed_rednered_template = fixed_rednered_template.replace('../../../media/uploads', 'media')
    fixed_rednered_template = fixed_rednered_template.replace('/staticfiles/js', 'js/')
    media_sources = re.findall('src="([^"]+)"', fixed_rednered_template)
    files_to_download = []
    for media_source in media_sources:
        if media_source.startswith('media/'):
            files_to_download.append( media_source[6:] )
    #usunac jesli istnieje
    zipdata = StringIO()
   # zipfilename = settings.MEDIA_ROOT+'/zipped_presentations/presentation.zip'
    zf = zipfile.ZipFile(zipdata, mode='w')
    try:
        presentation_filename = settings.MEDIA_ROOT + 'presentation.html'
        presentation_file = open(presentation_filename, 'w')
        presentation_file.write(fixed_rednered_template)
        presentation_file.close()
        zf.write(presentation_filename, 'presentation.html')
        
        zf.write(settings.STATIC_ROOT + '/js/impress.js', 'js/impress.js')
        
        for media_file in files_to_download:
            zf.write(settings.MEDIA_ROOT+'/uploads/'+media_file, 'media/'+media_file)
    finally:
        zf.close()
        zipdata.seek(0)

    
    response = HttpResponse(zipdata.read())
    response['Content-Disposition'] = 'attachment; filename=presentation.zip'
    response['Content-Type'] = 'application/x-zip'
    return response


def add_slide(request, presentation_id):
    
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
    else:
        slide_form = SlideForm()
        position_form = PositionForm()
    ctx = {
           'presentation_id': presentation.id,
           'success': success,
           'slide_form': slide_form,
           'position_form': position_form,
           "presentation": presentation,
    }
    
    return render_to_response('presentation/add_slide.html', ctx)

def edit_slide(request, presentation_id, slide_id):
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    slide =  get_object_or_404(Slide, pk=slide_id)
    position = get_object_or_404(Position, pk=slide_id)
    success = False
    
    slide_form = SlideForm(instance=slide)
    position_form = PositionForm(instance=position)
    
    if request.method == "POST":
        s_form = SlideForm(request.POST, instance=slide)
        p_form = PositionForm(request.POST, instance=position)
        if s_form.is_valid() and p_form.is_valid():
            s_form.save()
            p_form.save()
        success = True
    
    ctx = {
         "slide_form": slide_form,
         "position_form": position_form,
         "success": success,
         "edit": True,
         "presentation": presentation,
    }
    return render_to_response('presentation/add_slide.html', ctx)

def delete_slide(request, presentation_id, slide_id):
    confirmation = False
    slide = get_object_or_404(Slide, pk=slide_id)
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    
    if request.method == "POST" and request.POST['confirm'] == 'Tak':
        slide_order_nb = slide.order_number
        slide.delete()
        Slide.repair_slide_order(presentation_id, slide_order_nb)
        
        confirmation = True
    ctx = {
           'confirmation': confirmation,
           'slide': slide,
           'presentation': presentation,
    }    
    return render_to_response('presentation/delete_slide.html', ctx)

def preview_slide(request, presentation_id, slide_id):
    slide = get_object_or_404(Slide, pk=slide_id)
    presentation = get_object_or_404(Presentation, pk=presentation_id)
    position = get_object_or_404(Position, pk=slide_id)
    
    ctx = {
           'slide': slide,
           'presentation': presentation,
           'position': position,
    }
    return render_to_response('presentation/preview_slide.html', ctx)

def generate_slide_preview(request, slide_id):
    slide = get_object_or_404(Slide, pk=slide_id)
    position = get_object_or_404(Position, pk=slide_id)
    ctx = {
           'slide': slide,
           'position': position,
    }
    return render_to_response('presentation/generate_slide_preview.html', ctx)

def move_slide(request, slide_id, direction):
    slide = get_object_or_404(Slide, pk=slide_id)
    slide_to_move_up = None
    slide_to_move_down = None
    
    if not ( (direction == 'up' and slide.is_first()) or (direction == 'down' and slide.is_last()) ):
        if direction == 'up':
            slide_to_move_up = slide
            slide_to_move_down = Slide.objects.get(presentation=slide.presentation.id, order_number=slide.order_number-1)
        else:
            slide_to_move_down = slide
            slide_to_move_up = Slide.objects.get(presentation=slide.presentation.id, order_number=slide.order_number+1)
        print "slide to move up: %d", slide_to_move_up.id
        print "slide to move down: %D", slide_to_move_down.id
        Slide.swich_slides_order(slide_to_move_up, slide_to_move_down)
    return redirect(slide.presentation.get_details_url())
    
def copy_presentation_content(request, presentation_id=None):
    
    ctx = None
    if presentation_id:
        presentation = get_object_or_404(Presentation, pk=presentation_id)
        slides = Slide.objects.filter(presentation=presentation)
        ctx = {'slides':slides,
               'presentation_chosen': True}
    else:
        presentations = Presentation.objects.all()
        ctx =  {'presentations': presentations,}
    
    return render_to_response('presentation/copy_presentation_content.html', ctx)
        
def get_slide_content(request, slide_id):
    slide = get_object_or_404(Slide, pk=slide_id)
    data_to_return = {
        'success': True,
        'content': slide.content,
        'description': slide.description,
    }

    return HttpResponse(simplejson.dumps(data_to_return, ensure_ascii=False), mimetype='application/json')
    
    
    