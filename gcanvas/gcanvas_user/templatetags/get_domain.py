from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(name='show_domain')
def get_domain(*args, **kwargs):
    try:
        return settings.DOMAIN
    except:
        return ''
