from django import template
from engineerThesis.presentation.models import Slide, Position
from django.shortcuts import get_object_or_404

register = template.Library()

@register.inclusion_tag('presentation/templatetags/slide_preview.html')
def render_slide_preview(slide_id):
    slide =  get_object_or_404(Slide, pk=slide_id)
    position = get_object_or_404(Position, pk=slide_id)
    return {'slide': slide,
            'position': position
        }
      
