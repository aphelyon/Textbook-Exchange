from django.shortcuts import render, HttpResponseRedirect, reverse
from django.http import JsonResponse
import urllib.request
import urllib.parse
import json
from datetime import datetime
import webapp.forms
import http.cookies
from ast import literal_eval


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


#def get_user_pk(request):



def create_textbook_view(request):
    auth = request.COOKIES.get('auth')
    textbook_form = webapp.forms.textbookForm()
    if not auth:
        # Handle user not logged in while trying to create a listing
        return HttpResponseRedirect(reverse("webapp:login"))
    if request.method == 'GET':
        # Return to form page
        return render(request, 'textbook.html', {'form': textbook_form})

    f = webapp.forms.listingForm(request.POST)
    if not f.is_valid():
        return render(request, 'textbook.html', {'form': textbook_form})

def Create_listing_view(request):
    auth = request.COOKIES.get('auth')
    listing_form = webapp.forms.listingForm()
    if not auth:
        # Handle user not logged in while trying to create a listing
        return HttpResponseRedirect(reverse("webapp:login"))
    if request.method == 'GET':
        # Return to form page
        return render(request, 'listing.html', {'form': listing_form})

    f = webapp.forms.listingForm(request.POST)
    if not f.is_valid():
        return render(request, 'listing.html', {'form': listing_form})

    authenticator = literal_eval(request.COOKIES.get('auth').replace('&',','))
    k = authenticator['user_id']

    item = f.cleaned_data['item']
    price = f.cleaned_data['price']
    user = k
    condition = f.cleaned_data['condition']
    status = f.cleaned_data['status']
    experience_url = 'http://exp-api:8000/experience/listings'
    data = urllib.parse.urlencode({'item': item, 'price': price, 'condition': condition, 'user': user, 'status': status}).encode('utf-8')
    experience_request = urllib.request.Request(experience_url, data)
    experience_response = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
    if not experience_response or not experience_response['create_listing']['ok']:
        if experience_response['create_listing']['error'] == 'exp_srvc_errors.E_UNKNOWN_AUTH':
            return HttpResponseRedirect(reverse("webapp:login"))
        return render(request, "create_listing_fail.html", {'form': listing_form})
        #return experience_response
    return listing_view(request, experience_response['create_listing']['results']['pk'])

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
    next_page = ret_form.cleaned_data.get('next') or reverse('webapp:index')
    authenticator = str(experience_response['results']['authenticator']).replace(',','&')
    response = HttpResponseRedirect(next_page)
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

    first_name = ret_form.cleaned_data['first_name']
    last_name = ret_form.cleaned_data['last_name']
    email = ret_form.cleaned_data['email']
    username = ret_form.cleaned_data['username']
    password = ret_form.cleaned_data['password']
    experience_url = 'http://exp-api:8000/experience/signup'
    datadict = {'first_name': first_name, 'last_name': last_name, 'email': email, 'username': username,
                'password': password}
    data = urllib.parse.urlencode(datadict).encode('utf-8')
    experience_request = urllib.request.Request(experience_url, data)
    experience_response = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
    if not experience_response['ok']:
        if "for key 'email'" in experience_response['error']:
            ret_form.add_error('email', "Email provided is already in use")
        elif "for key 'username'" in experience_response['error']:
            ret_form.add_error('username', "Username provided is already in use")
        return render(request, 'signup.html', {'form': ret_form})
    else:
        experience_login_url = 'http://exp-api:8000/experience/login'
        data = urllib.parse.urlencode({'username': username, 'password': password}).encode('utf-8')
        experience_request = urllib.request.Request(experience_login_url, data)
        experience_login_response = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
        if not experience_login_response or not experience_login_response['ok']:
            return HttpResponseRedirect(reverse("webapp:login"))
        else:
            response = HttpResponseRedirect(reverse('webapp:index'))
            response.set_cookie('auth', str(experience_login_response['results']['authenticator']).replace(',', '&'))
            return response

def logout(request):
    response = HttpResponseRedirect(reverse('webapp:index'))
    if request.method == "POST":
        authenticator = literal_eval(request.COOKIES.get('auth').replace('&',','))
        if authenticator:
            experience_url = 'http://exp-api:8000/experience/logout'
            data = urllib.parse.urlencode({'authenticator': authenticator['authenticator']}).encode('utf-8')
            experience_request = urllib.request.Request(experience_url, data)
            experience_response = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
            # Not sure if we care if the cookie is invalid
            response.delete_cookie('auth')
    return response
