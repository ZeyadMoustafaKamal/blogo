from django import template

register = template.Library()

@register.filter
def split(value,seperator=','):
    return value.split(seperator)
@register.filter
def replace(value,old='_',new=' '):
    return value.replace(old,new)
