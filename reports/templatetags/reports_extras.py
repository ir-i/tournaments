
from django import template



register = template.Library()


@register.filter
def getkey(dictionary, key):
    return dictionary.get(key, '')