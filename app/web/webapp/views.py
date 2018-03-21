from django.shortcuts import render, HttpResponseRedirect, reverse
from django.http import JsonResponse
import urllib.request
import urllib.parse
import json
from datetime import datetime
import webapp.forms
import http.cookies


# Create your views here.

def index(request):
    experience_url = 'http://exp-api:8000/experience/home'
    experience_request = urllib.request.Request(experience_url)
    page_details = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
    return render(request, 'index.html', page_details)


def listing_view(request, pk):
    """Right now, this just returns the details of a listing and nothing else"""
    request_url = 'http://exp-api:8000/experience/listings/' + str(pk)
    experience_request = urllib.request.Request(request_url)
    # This is from the code in the write-up
    listing_details = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
    # Set up our date to be a datetime object, so that it will actually look pretty to the user
    if 'results' in listing_details:
        listing_details['results']['item']['pub_date'] = datetime.strptime(listing_details['results']['item']
                                                                           ['pub_date'][:-6], "%Y-%m-%d %H:%M:%S")
    return render(request, 'listing_detail.html', listing_details)


def user_profile_view(request, pk):
    experience_url = 'http://exp-api:8000/experience/users/' + str(pk)
    experience_request = urllib.request.Request(experience_url)
    user_details = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
    if 'results' in user_details:
        user_details['results']['userJoined'] = datetime.strptime(user_details['results']['userJoined'][:-6], "%Y-%m-%d %H:%M:%S")
    return render(request, 'user_profile.html', user_details)


def course_view(request, pk):
    experience_url = 'http://exp-api:8000/experience/courses/' + str(pk)
    experience_request = urllib.request.Request(experience_url)
    course_details = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
    return render(request, 'course_detail.html', course_details)


def textbook_view(request, pk):
    experience_url = 'http://exp-api:8000/experience/textbooks/' + str(pk)
    experience_request = urllib.request.Request(experience_url)
    textbook_details = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
    if 'textbook' in textbook_details:
        textbook_details['textbook']['results']['pub_date'] = datetime.strptime(textbook_details['textbook']['results']['pub_date'][:-6], "%Y-%m-%d %H:%M:%S")
    return render(request, 'textbook_detail.html', textbook_details)


def login(request):
    form = webapp.forms.LoginForm()
    if request.method == "GET":
        return render(request, 'login.html', {'form': form})

    ret_form = webapp.forms.LoginForm(request.POST)

    if not ret_form.is_valid():
        return render(request, 'login.html', {'form': ret_form})

    username = ret_form.cleaned_data['username']
    password = ret_form.cleaned_data['password']
    experience_url = 'http://exp-api:8000/experience/login'
    data = urllib.parse.urlencode({'username': username, 'password': password}).encode('utf-8')
    experience_request = urllib.request.Request(experience_url, data)
    experience_response = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
    if not experience_response or not experience_response['ok']:
        ret_form.add_error('username', 'Username and password do not match')
        return render(request, 'login.html', {'form': ret_form})
    authenticator = experience_response['results']['authenticator']['authenticator']
    response = HttpResponseRedirect(reverse('webapp:index'))
    response.set_cookie("auth", authenticator)

    return response


def signup(request):
    form = webapp.forms.SignUpForm()
    if request.method == "GET":
        return render(request, 'signup.html', {'form': form})

    ret_form = webapp.forms.SignUpForm(request.POST)
    if not ret_form.is_valid():
        return render(request, 'signup.html', {'form': ret_form})
    if ret_form.cleaned_data['password'] != ret_form.cleaned_data['confirm_password']:
        ret_form.add_error('confirm_password', 'Passwords must match.')
        return render(request, 'signup.html', {'form': ret_form})


def logout(request):
    response = HttpResponseRedirect(reverse('webapp:index'))
    if request.method == "POST":
        authenticator = request.COOKIES.get('auth')
        if authenticator:
            experience_url = 'http://exp-api:8000/experience/logout'
            data = urllib.parse.urlencode({'authenticator': authenticator}).encode('utf-8')
            experience_request = urllib.request.Request(experience_url, data)
            experience_response = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
            # Not sure if we care if the cookie is invalid
            response.delete_cookie('auth')
    return response
