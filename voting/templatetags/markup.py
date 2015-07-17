import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='markup')
def markup(value):
    if value is None:
        return value
    return mark_safe(markdown.markdown(value))
