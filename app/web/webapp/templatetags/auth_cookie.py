"""Lets you see if the user is logged in in a Django template"""
from django import template

register = template.Library()


@register.simple_tag(takes_context=True, name='cookies')
def cookies(context):
    request = context['request']
    result = request.COOKIES.get('auth', '')
    return 'dude'
