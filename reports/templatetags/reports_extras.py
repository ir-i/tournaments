
from django import template



register = template.Library()



@register.filter
def getkey(dictionary, key):
    return dictionary.get(key, '')



@register.inclusion_tag('reports/report.html', takes_context=True)
def report(context):
    return {
        'request': context['request'],
        'report': context['report'],
    }