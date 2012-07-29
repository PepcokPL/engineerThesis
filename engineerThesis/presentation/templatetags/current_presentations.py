from django import template
from engineerThesis.presentation.models import Presentation

register = template.Library()

@register.inclusion_tag('presentation/templatetags/current_presentations.html')
def current_presentations():
    presentations = Presentation.objects.all()
    return {'current_presentations': presentations}
      
