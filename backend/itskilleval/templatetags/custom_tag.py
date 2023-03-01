from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    if type(value) is not str:
        raise ValueError()
    return value.split(arg)