from django.shortcuts import render
from django.shortcuts import HttpResponse
import urllib.request
from urllib import parse
import json


# Create your views here.

def listing_view(request, pk):
    request_url = 'http://models-api:8000/api/v1/listings/' + str(pk)
    database_request = urllib.request.Request(request_url)
    # This is from the code in the write-up
    response = json.loads(urllib.request.urlopen(database_request).read().decode('utf-8'))
    return HttpResponse(json.dumps(response), content_type='application/json')
