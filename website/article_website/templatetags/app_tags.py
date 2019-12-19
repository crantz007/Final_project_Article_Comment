from django import template

register = template.Library()


@register.filter(is_safe=True)
def capitalize(text):
    return text.title()
