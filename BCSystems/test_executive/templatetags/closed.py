from django import template
register = template.Library()

@register.filter
def closed(indexable, i):
    return indexable[i]