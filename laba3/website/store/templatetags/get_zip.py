from django import template

register = template.Library()


@register.filter()
def get_zip(start, end):
    return zip(start, end)
