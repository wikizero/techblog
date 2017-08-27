from django import template
__author__ = 'admin'
register = template.Library()


@register.simple_tag
def sum(a, b):
    try:
        return a + b
    except Exception, e:
        return e

