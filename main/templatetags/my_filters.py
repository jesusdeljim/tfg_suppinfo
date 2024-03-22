from django import template

register = template.Library()


@register.filter(name="to")
def to(value, arg):
    """Genera rangos de números desde value hasta arg."""
    return range(value, arg + 1)

@register.filter(name='user_list')
def user_list(value):
    return ", ".join(str(user) for user in value)