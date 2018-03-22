from django.shortcuts import render
from django.http import JsonResponse
import urllib.request
import urllib.parse
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


def get_textbook_view(request):
    get_textbooks_url = 'http://models-api:8000/api/v1/textbooks/get_all'
    get_textbooks_request = urllib.request.Request(get_textbooks_url)
    get_textbooks_response = json.loads(urllib.request.urlopen(get_textbooks_request).read().decode('utf-8'))
    return JsonResponse({'get_textbooks': get_textbooks_response})

def get_courses_view(request):
    get_courses_url = 'http://models-api:8000/api/v1/courses/get_all'
    get_courses_request = urllib.request.Request(get_courses_url)
    get_courses_response = json.loads(urllib.request.urlopen(get_courses_request).read().decode('utf-8'))
    return JsonResponse({'get_courses': get_courses_response})

def get_professors_view(request):
    get_professors_url = 'http://models-api:8000/api/v1/professors/get_all'
    get_professors_request = urllib.request.Request(get_professors_url)
    get_professors_response = json.loads(urllib.request.urlopen(get_professors_request).read().decode('utf-8'))
    return JsonResponse({'get_professors': get_professors_response})


def Create_listing_view(request):
    create_listing_url = 'http://models-api:8000/api/v1/listings/create'
    #create_listing_request = urllib.request.Request(create_listing_url)
    #create_listing_response = json.loads(urllib.request.urlopen(create_listing_request).read().decode('utf-8'))
    data = urllib.parse.urlencode(
        {'textbook_key': request.POST.get('item'), 'price': request.POST.get('price'), 'user_key': request.POST.get('user'),
         'condition': request.POST.get('condition'), 'status': request.POST.get('status')}).encode('utf-8')
    create_request = urllib.request.Request(create_listing_url, data)
    response = json.loads(urllib.request.urlopen(create_request).read().decode('utf-8'))
    return JsonResponse({'create_listing': response})

def create_textbook_view(request):
    create_textbook_url = 'http://models-api:8000/api/v1/textbooks/create'
    data = urllib.parse.urlencode(
        {'professor_key': request.POST.get('item'), 'price': request.POST.get('price'), 'user_key': request.POST.get('user'),
         'condition': request.POST.get('condition'), 'status': request.POST.get('status')}).encode('utf-8')
    create_request = urllib.request.Request(create_textbook_url, data)
    response = json.loads(urllib.request.urlopen(create_request).read().decode('utf-8'))
    return JsonResponse({'create_textbook': response})

def create_professor_view(request):
    create_professor_url = 'http://models-api:8000/api/v1/professors/create'
    data = urllib.parse.urlencode(
        {'name': request.POST.get('name'), 'email': request.POST.get('email'), 'status': request.POST.get('status')}).encode('utf-8')
    create_request = urllib.request.Request(create_professor_url, data)
    response = json.loads(urllib.request.urlopen(create_request).read().decode('utf-8'))
    return JsonResponse({'create_professor': response})

def homepage_view(request):
    most_viewed_listings_url = 'http://models-api:8000/api/v1/listings/most_viewed'
    most_viewed_courses_url = 'http://models-api:8000/api/v1/courses/most_viewed'
    most_viewed_listings_request = urllib.request.Request(most_viewed_listings_url)
    most_viewed_listings_response = json.loads(urllib.request.urlopen(most_viewed_listings_request).read().decode('utf-8'))
    most_viewed_courses_request = urllib.request.Request(most_viewed_courses_url)
    most_viewed_courses_response = json.loads(urllib.request.urlopen(most_viewed_courses_request).read().decode('utf-8'))
    newest_url = 'http://models-api:8000/api/v1/listings/newest'
    newest_request = urllib.request.Request(newest_url)
    newest_response = json.loads(urllib.request.urlopen(newest_request).read().decode('utf-8'))
    return JsonResponse({'most_viewed': most_viewed_listings_response, 'newest': newest_response, 'most_viewed_courses': most_viewed_courses_response})


def user_profile_view(request, pk):
    database_request_url = 'http://models-api:8000/api/v1/users/' + str(pk)
    database_request = urllib.request.Request(database_request_url)
    response = json.loads(urllib.request.urlopen(database_request).read().decode('utf-8'))
    return JsonResponse(response)


def course_view(request, pk):
    increment_request_url = 'http://models-api:8000/api/v1/courses/' + str(pk) + '/incrementCount'
    database_request_url = 'http://models-api:8000/api/v1/courses/' + str(pk)
    textbook_url = 'http://models-api:8000/api/v1/textbooks/from_course/' + str(pk)
    # Request to increment the listing view count
    urllib.request.urlopen(urllib.request.Request(increment_request_url))
    database_request = urllib.request.Request(database_request_url)
    textbook_request = urllib.request.Request(textbook_url)
    # This is from the code in the write-up
    response = json.loads(urllib.request.urlopen(database_request).read().decode('utf-8'))
    textbook_response = json.loads(urllib.request.urlopen(textbook_request).read().decode('utf-8'))
    return JsonResponse({'course':response, 'textbooks': textbook_response})


def textbook_view(request, pk):
    database_request_url = 'http://models-api:8000/api/v1/textbooks/' + str(pk)
    listing_url = 'http://models-api:8000/api/v1/listings/from_textbook/' + str(pk)
    database_request = urllib.request.Request(database_request_url)
    listing_request = urllib.request.Request(listing_url)
    response = json.loads(urllib.request.urlopen(database_request).read().decode('utf-8'))
    listing_response = json.loads(urllib.request.urlopen(listing_request).read().decode('utf-8'))
    return JsonResponse({'textbook': response, 'listings': listing_response})


def login(request):
    login_request_url = 'http://models-api:8000/api/v1/users/login'
    data = urllib.parse.urlencode({'username': request.POST.get('username'), 'password': request.POST.get('password')}).encode('utf-8')
    login_request = urllib.request.Request(login_request_url, data)
    response = json.loads(urllib.request.urlopen(login_request).read().decode('utf-8'))
    return JsonResponse(response)


def logout(request):
    database_request_url = 'http://models-api:8000/api/v1/authenticators/delete'
    data = urllib.parse.urlencode({'authenticator': request.POST.get('authenticator')}).encode('utf-8')
    database_request = urllib.request.Request(database_request_url, data)
    response = json.loads(urllib.request.urlopen(database_request).read().decode('utf-8'))
    return JsonResponse(response)


def signup(request):
    database_request_url = 'http://models-api:8000/api/v1/users/create'
    data = urllib.parse.urlencode(request.POST).encode('utf-8')
    database_request = urllib.request.Request(database_request_url, data)
    response = json.loads(urllib.request.urlopen(database_request).read().decode('utf-8'))
    return JsonResponse(response)
