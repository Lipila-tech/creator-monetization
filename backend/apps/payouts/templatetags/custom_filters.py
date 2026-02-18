from django import template

register = template.Library()

@register.filter
def absolute(value):
    """Return the absolute value of a number."""
    return abs(value)