from django.shortcuts import render
import urllib.request
import json
from datetime import datetime

# Create your views here.

def index(request):
    return render(request, 'index.html')


def listing_view(request, pk):
    """Right now, this just returns the details of a listing and nothing else"""
    request_url = 'http://exp-api:8000/experience/listings/' + str(pk)
    experience_request = urllib.request.Request(request_url)
    # This is from the code in the write-up
    listing_details = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
    if 'error' in listing_details:
        listing_details['does_not_exist'] = True
        return render(request, 'listing_detail.html', listing_details)
    else:
        listing_details['listing']['item']['pub_date'] = datetime.strptime(listing_details['listing']['item']['pub_date'][:-6], "%Y-%m-%d %H:%M:%S")

        return render(request, 'listing_detail.html', listing_details['listing'])
