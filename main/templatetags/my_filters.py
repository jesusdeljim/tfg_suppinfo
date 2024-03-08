from django import template

register = template.Library()

@register.filter(name='to')
def to(value, arg):
    """Genera rangos de números desde value hasta arg."""
    return range(value, arg + 1)