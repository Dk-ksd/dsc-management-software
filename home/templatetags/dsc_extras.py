from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter  # Handles string inputs gracefully
def get_item(value, key):
    if hasattr(value, 'get'):  # Works for dict-like objects
        return value.get(key, '')
    return ''