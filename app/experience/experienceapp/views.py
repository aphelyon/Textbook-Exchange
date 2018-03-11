from django.shortcuts import render
from django.http import JsonResponse
import urllib.request
from urllib import parse
import json


# Create your views here.

def listing_view(request, pk):
    """Right now, this just returns the details of a listing, increments its count and nothing else"""
    increment_request_url = 'http://models-api:8000/api/v1/listings/' + str(pk) + '/incrementCount'
    database_request_url = 'http://models-api:8000/api/v1/listings/' + str(pk)
    # Request to increment the listing view count
    urllib.request.urlopen(urllib.request.Request(increment_request_url))
    database_request = urllib.request.Request(database_request_url)
    # This is from the code in the write-up
    response = json.loads(urllib.request.urlopen(database_request).read().decode('utf-8'))
    return JsonResponse(response)


def homepage_view(request):
    most_viewed_url = 'http://models-api:8000/api/v1/listings/most_viewed'
    most_viewed_request = urllib.request.Request(most_viewed_url)
    most_viewed_response = json.loads(urllib.request.urlopen(most_viewed_request).read().decode('utf-8'))
    return JsonResponse({'most_viewed': most_viewed_response})
