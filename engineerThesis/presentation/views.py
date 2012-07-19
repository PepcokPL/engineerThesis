from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import Presentation  


def index(request):
    presentations = Presentation.objects.all()
    ctx = { 'presentations': presentations}
    return render_to_response('presentation/index.html', ctx)

def presentations(request):
    presentations = Presentation.objects.all()
    ctx = { 'presentations': presentations}
    return render_to_response('presentation/presentations.html', ctx)

def add_presentation(request):
    presentations = Presentation.objects.all()
    ctx = { 'presentations': presentations}
    return render_to_response('presentation/add_presentation.html', ctx)