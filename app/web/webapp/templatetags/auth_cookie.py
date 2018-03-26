"""Lets you see if the user is logged in in a Django template"""
from django import template
import urllib.parse
import urllib.request
from ast import literal_eval
import json

register = template.Library()


@register.simple_tag(takes_context=True, name='cookies')
def cookies(context):
    request = context['request']
    result = request.COOKIES.get('auth', '')
    if result:
        experience_url = 'http://exp-api:8000/experience/navbar'
        authenticator = literal_eval(result.replace('&', ','))
        data = urllib.parse.urlencode({'authenticator': authenticator['authenticator']}).encode('utf-8')
        experience_request = urllib.request.Request(experience_url, data)
        experience_response = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
        return experience_response['ok']
    else:
        return False
