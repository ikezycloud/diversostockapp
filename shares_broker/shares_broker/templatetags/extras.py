from django import template

@register.filter
def lower(value):
    return value.lower()