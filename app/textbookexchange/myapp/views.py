from django.shortcuts import render
from django.shortcuts import HttpResponse
from myapp.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from django.views.decorators.http import require_POST, require_GET
import json

# Create your views here.


def details_user(request, pk):
    pass


def create_user(request):
    pass


def delete_user(request, pk):
    try:
        User.objects.get(pk=pk).delete()
        return HttpResponse(json.dumps({"Status": "200"}))
    except User.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested User object does not exist"}),
                            content_type='application/json')


# This method is for getting a professor's details and or updating them. I couldn't think of a better name to encompass
# both things
def details_professor(request, pk):
    try:
        retrieved_professor = Professor.objects.get(pk=pk)

        if request.method == "POST":
            try:
                data = json.loads(request.body.decode('utf-8'))
                try:
                    retrieved_professor.name = data['name']
                except KeyError:
                    print("Name not sent in json POST request")
                try:
                    retrieved_professor.email = data['email']
                except KeyError:
                    print("Email not sent in json POST request")
                retrieved_professor.save()

            except ValueError:  # Means that JSON was not a part of the request
                return HttpResponse(json.dumps({"Error": "JSON object not sent as part of POST request"}),
                            content_type='application/json')

        response = retrieved_professor.as_json()
        response.update({"status": "200"})
        return HttpResponse(json.dumps(response), content_type='application/json')

    except Professor.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested Professor object does not exist"}),
                            content_type='application/json')


@require_POST
def create_professor(request):
    data = json.loads(request.body.decode('utf-8'))
    new_professor = Professor.objects.create(name=data['name'], email=data['email'])
    return HttpResponse(json.dumps(new_professor.as_json()), content_type='application/json')


@require_POST
def delete_professor(request, pk):
    try:
        Professor.objects.get(pk=pk).delete()
        return HttpResponse(json.dumps({"Status": "200"}))
    except Professor.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested Professor object does not exist"}),
                            content_type='application/json')


def details_course(request, pk):
    pass


def create_course(request):
    pass


def delete_course(request, pk):
    try:
        Course.objects.get(pk=pk).delete()
        return HttpResponse(json.dumps({"Status": "200"}))
    except Course.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested Course object does not exist"}),
                            content_type='application/json')


def details_textbook(request, pk):
    pass


def create_textbook(request):
    pass


def delete_textbook(request, pk):
    try:
        Textbook.objects.get(pk=pk).delete()
        return HttpResponse(json.dumps({"Status": "200"}))
    except Textbook.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested Textbook object does not exist"}),
                            content_type='application/json')


def details_listing(request, pk):
    pass


def create_listing(request):
    pass


def delete_listing(request, pk):
    try:
        Listing.objects.get(pk=pk).delete()
        return HttpResponse(json.dumps({"Status": "200"}))
    except Listing.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested Listing object does not exist"}),
                            content_type='application/json')
