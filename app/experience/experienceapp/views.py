from django.shortcuts import render
from django.http import JsonResponse
import urllib.request
import urllib.parse
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch


# Create your views here.

def listing_view(request, pk):
    """Right now, this just returns the details of a listing, increments its count and nothing else"""
    increment_request_url = 'http://models-api:8000/api/v1/listings/' + str(pk) + '/incrementCount'
    recommendations_request_url = 'http://models-api:8000/api/v1/recommendations/' + str(pk)
    database_request_url = 'http://models-api:8000/api/v1/listings/' + str(pk)
    # Request to increment the listing view count
    urllib.request.urlopen(urllib.request.Request(increment_request_url))
    database_request = urllib.request.Request(database_request_url)
    recommendations_request = urllib.request.Request(recommendations_request_url)
    # This is from the code in the write-up
    response = json.loads(urllib.request.urlopen(database_request).read().decode('utf-8'))
    response2 = json.loads(urllib.request.urlopen(recommendations_request).read().decode('utf-8'))

    # Don't log if the user is not logged in
    if response['ok'] and 'user_id' in request.POST:
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        user_view = {'item_id': response['results']['pk'], 'user_id': request.POST.get('user_id')}
        producer.send('new-recommendations-topic', json.dumps(user_view).encode('utf-8'))

    response['results']['recommended_flag'] = response2['ok']

    if response2['ok']:
        recommendations = []
        response['results']['recommended_pk_list'] = response2['results']['recommended_items'].split(',')
        for item in range(1, len(response['results']['recommended_pk_list'])):
            response['results']['recommended_pk_list'][item] = response['results']['recommended_pk_list'][item][1:]
        for listing_pk in response['results']['recommended_pk_list']:
            database_request_url = 'http://models-api:8000/api/v1/listings/' + str(listing_pk)
            database_request = urllib.request.Request(database_request_url)
            response3 = json.loads(urllib.request.urlopen(database_request).read().decode('utf-8'))
            recommendations.append(response3)
        response['results']['recommendations'] = recommendations
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


def search_view(request):
    data = request.GET.get('search')
    es = Elasticsearch(['es'])
    response = es.search(index='listing_index', body={'query': {'query_string': {'query': data}}, 'size': 10})
    return JsonResponse({'search': response})


def Create_listing_view(request):
    authenticate_url = 'http://models-api:8000/api/v1/authenticators/check'
    authenticate_data = urllib.parse.urlencode({'authenticator': request.POST.get('authenticator')}).encode('utf-8')
    authenticate_request = urllib.request.Request(authenticate_url, authenticate_data)
    authenticate_response = json.loads(urllib.request.urlopen(authenticate_request).read().decode('utf-8'))
    if not authenticate_response['ok']:
        # The current user is not authenticated to create a new listing, don't let the request go through
        return JsonResponse({'create_listing': authenticate_response})
    create_listing_url = 'http://models-api:8000/api/v1/listings/create'

    data = urllib.parse.urlencode({'textbook_key': request.POST.get('item'), 'price': request.POST.get('price'), 'user_key':
        request.POST.get('user'), 'condition': request.POST.get('condition'), 'status': request.POST.get('status')}).encode('utf-8')
    create_request = urllib.request.Request(create_listing_url, data)
    response = json.loads(urllib.request.urlopen(create_request).read().decode('utf-8'))

    # Add kafka queue stuff
    if response['ok']:
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        # Because course is optional for a textbook
        if 'course' in response['results']:
            data_dict = {'title': response['results']['item']['title'], 'price': response['results']['price_text'],
                         'user': response['results']['user']['username'], 'user_pk': response['results']['user']['pk'], 'condition': response['results']['condition'],
                         'status': response['results']['status'], 'id': response['results']['pk'],
                         'course': response['results']['item']['course']['identifier'],
                         'course_department': response['results']['item']['course']['department'],
                         'isbn': response['results']['item']['ISBN'], 'pub_date': response['results']['item']['pub_date']}
        else:
            data_dict = {'title': response['results']['item']['title'], 'price': response['results']['price_text'],
                         'user': response['results']['user']['username'], 'user_pk': response['results']['user']['pk'], 'condition': response['results']['condition'],
                         'status': response['results']['status'], 'id': response['results']['pk'],
                         'isbn': response['results']['item']['ISBN'], 'pub_date': response['results']['item']['pub_date']}
        producer.send('new-listings-topic', json.dumps(data_dict).encode('utf-8'))

    return JsonResponse({'create_listing': response})


def create_course_view(request):
    authenticate_url = 'http://models-api:8000/api/v1/authenticators/check'
    authenticate_data = urllib.parse.urlencode({'authenticator': request.POST.get('authenticator')}).encode('utf-8')
    authenticate_request = urllib.request.Request(authenticate_url, authenticate_data)
    authenticate_response = json.loads(urllib.request.urlopen(authenticate_request).read().decode('utf-8'))
    if not authenticate_response['ok']:
        # The current user is not authenticated to create a new listing, don't let the request go through
        return JsonResponse({'create_course': authenticate_response})
    create_listing_url = 'http://models-api:8000/api/v1/courses/create'
    data = urllib.parse.urlencode(
        {'name': request.POST.get('name'), 'identifier': request.POST.get('identifier'), 'department': request.POST.get('department'),
         'professor_key': request.POST.get('professor')}).encode('utf-8')
    create_request = urllib.request.Request(create_listing_url, data)
    response = json.loads(urllib.request.urlopen(create_request).read().decode('utf-8'))
    return JsonResponse({'create_course': response})


def create_textbook_view(request):
    authenticate_url = 'http://models-api:8000/api/v1/authenticators/check'
    authenticate_data = urllib.parse.urlencode({'authenticator': request.POST.get('authenticator')}).encode('utf-8')
    authenticate_request = urllib.request.Request(authenticate_url, authenticate_data)
    authenticate_response = json.loads(urllib.request.urlopen(authenticate_request).read().decode('utf-8'))
    if not authenticate_response['ok']:
        # The current user is not authenticated to create a new listing, don't let the request go through
        return JsonResponse({'create_textbook': authenticate_response})
    create_textbook_url = 'http://models-api:8000/api/v1/textbooks/create'
    data = urllib.parse.urlencode(
        {'item_title': request.POST.get('title'), 'item_author': request.POST.get('author'), 'course_key': request.POST.get('course'),
         'item_ISBN': request.POST.get('isbn'), 'pub_date': request.POST.get('pub_date')}).encode('utf-8')
    create_request = urllib.request.Request(create_textbook_url, data)
    response = json.loads(urllib.request.urlopen(create_request).read().decode('utf-8'))
    return JsonResponse({'create_textbook': response})


def create_professor_view(request):
    authenticate_url = 'http://models-api:8000/api/v1/authenticators/check'
    authenticate_data = urllib.parse.urlencode({'authenticator': request.POST.get('authenticator')}).encode('utf-8')
    authenticate_request = urllib.request.Request(authenticate_url, authenticate_data)
    authenticate_response = json.loads(urllib.request.urlopen(authenticate_request).read().decode('utf-8'))
    if not authenticate_response['ok']:
        # The current user is not authenticated to create a new listing, don't let the request go through
        return JsonResponse({'create_professor': authenticate_response})
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


def my_listing_view(request, pk):
    my_listing_request_url = 'http://models-api:8000/api/v1//listings/from_user/' + str(pk)
    my_listing_request = urllib.request.Request(my_listing_request_url)
    response = json.loads(urllib.request.urlopen(my_listing_request).read().decode('utf-8'))
    return JsonResponse({'my_listings': response})


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


def nav_bar(request):
    authenticator_check_url = 'http://models-api:8000/api/v1/authenticators/check'
    data = urllib.parse.urlencode(request.POST).encode('utf-8')
    authenticator_request = urllib.request.Request(authenticator_check_url, data)
    response = json.loads(urllib.request.urlopen(authenticator_request).read().decode('utf-8'))
    return JsonResponse(response)

