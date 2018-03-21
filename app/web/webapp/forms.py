from django import forms
from webapp import views
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.http import JsonResponse
import urllib.request
import urllib.parse
import json
from datetime import datetime

class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput())


class listingForm(forms.Form):
    textbook_item = []
    i = 1
    while True:
        experience_url = 'http://exp-api:8000/experience/textbooks/' + str(i)
        experience_request = urllib.request.Request(experience_url)
        textbook_details = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
        if textbook_details['listings']['ok'] == False:
            break
        textbook_tuple = \
            (textbook_details['textbook']['results']['pk'], textbook_details['textbook']['results']['title'])
        textbook_item.append(textbook_tuple)
        i = i+1
    item = forms.CharField(label='which book', widget=forms.Select(choices=textbook_item))
    price = forms.CharField(max_length=32)
    user = forms.CharField(max_length=32)
    condition_of_textbook = (
        ('NEW', 'Brand new, unused Textbook'),
        ('USED_GOOD', 'Used, in good condition'),
        ('USED_OKAY', 'Used, in okay condition'),
        ('USED_POOR', 'Used, in poor condition')
    )
    condition = forms.CharField(label='condition of the item', widget=forms.Select(choices=condition_of_textbook))
    status_of_listing = (
        ('For Sale', 'For Sale'),
        ('Negotiation', 'Under Negotiation'),
        ('Sold', 'Sold')
    )
    status = forms.CharField(label='status of the item', widget=forms.Select(choices=status_of_listing))



class SignUpForm(forms.Form):
    email = forms.EmailField(max_length=100)
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=256, widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

