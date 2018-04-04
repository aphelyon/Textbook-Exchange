from django import template


register = template.Library()

@register.filter(name='get_under')
def get(d, k):
    return d.get(k, None)
