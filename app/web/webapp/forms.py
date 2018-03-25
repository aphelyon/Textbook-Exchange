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

class textbookForm(forms.Form):
    title = forms.CharField(max_length=200)
    author = forms.CharField(max_length=200)
    isbn = forms.CharField(max_length=200, label='ISBN Number')
    pub_date = forms.DateField(label='Publication Date')
    def __init__(self, *args, **kwargs):
        super(textbookForm, self, ).__init__(*args, **kwargs)
        course_items = []
        experience_url = 'http://exp-api:8000/experience/get_all_courses'
        experience_request = urllib.request.Request(experience_url)
        course_details = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
        for course in course_details['get_courses']['results']:
            pk = course['pk']
            identifier = course['identifier']
            tuple = (pk, identifier)
            course_items.append(tuple)
        self.fields['course'] = forms.CharField(widget=forms.Select(choices=course_items))
    #pub_date = forms.DateField('Publication Date', widget=forms.SelectDateWidget(years=range(2019,1970, -1)))

    
class listingForm(forms.Form):

    item = forms.CharField(widget=forms.Select(choices=[]))
    price = forms.DecimalField(decimal_places=2)
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

    def __init__(self, *args, **kwargs):
        super(listingForm, self,).__init__(*args, **kwargs)
        textbook_items = []
        experience_url = 'http://exp-api:8000/experience/get_all'
        experience_request = urllib.request.Request(experience_url)
        textbook_details = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
        for textbook in textbook_details['get_textbooks']['results']:
            pk = textbook['pk']
            title = textbook['title']
            tuple = (pk, title)
            textbook_items.append(tuple)
        self.fields['item'] = forms.CharField(widget=forms.Select(choices=textbook_items))



class SignUpForm(forms.Form):
    email = forms.EmailField(max_length=100)
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=256, widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

class courseForm(forms.Form):
    name = forms.CharField(max_length=100)
    identifier = forms.CharField(max_length=32)
    department = forms.CharField(max_length=100)
    def __init__(self, *args, **kwargs):
        super(courseForm, self, ).__init__(*args, **kwargs)
        experience_url = 'http://exp-api:8000/experience/get_all_professors'
        experience_request = urllib.request.Request(experience_url)
        professor_items = []
        professor_details = json.loads(urllib.request.urlopen(experience_request).read().decode('utf-8'))
        for professor in professor_details['get_professors']['results']:
            pk = professor['pk']
            prof_name = professor['name']
            tuple = (pk, prof_name)
            professor_items.append(tuple)
        self.fields['professor'] = forms.CharField(widget=forms.Select(choices=professor_items))

class professorForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
