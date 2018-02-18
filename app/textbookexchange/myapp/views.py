from django.shortcuts import render
from django.shortcuts import HttpResponse
from myapp.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from django.views.decorators.http import require_POST
import json
from django.core.exceptions import ValidationError

# Create your views here.


def details_user(request, pk):
    pass


@require_POST
def create_user(request):
    pass


@require_POST
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

        response = {"status":"200", "professor": retrieved_professor.as_json()}
        return HttpResponse(json.dumps(response), content_type='application/json')

    except Professor.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested Professor object does not exist"}),
                            content_type='application/json')


@require_POST
def create_professor(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        try:
            name = data['name']
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field name was not supplied"}),
                                content_type='application/json')
        try:
            email = data['email']
        except KeyError: # Email is not a required field
            new_professor = Professor.objects.create(name=name)
        else:
            new_professor = Professor.objects.create(name=name, email=email)

        response = {"status": "200", "professor": new_professor.as_json()}
        return HttpResponse(json.dumps(response), content_type='application/json')

    except ValueError:  # Means that JSON was not a part of the request
        return HttpResponse(json.dumps({"Error": "JSON object not sent as part of POST request"}),
                            content_type='application/json')



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


@require_POST
def create_course(request):
    pass


@require_POST
def delete_course(request, pk):
    try:
        Course.objects.get(pk=pk).delete()
        return HttpResponse(json.dumps({"Status": "200"}))
    except Course.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested Course object does not exist"}),
                            content_type='application/json')


def details_textbook(request, pk):
    try:
        retrieved_textbook = Textbook.objects.get(pk=pk)
        if request.method == "POST":

            try:
                data = json.loads(request.body.decode('utf-8'))
                try:
                    retrieved_textbook.item_title = data['item_title']
                except KeyError:
                    print("Title was not sent in JSON request")
                try:
                    retrieved_textbook.item_author = data['item_author']
                except KeyError:
                    print("Author was not sent in JSON request")
                try:
                    retrieved_textbook.item_ISBN = data['item_ISBN']
                except KeyError:
                    print("ISBN was not sent in JSON request")
                try:
                    retrieved_textbook.pub_date = data['pub_date']
                except KeyError:
                    print("Pub_date was not sent in JSON request")
                except ValidationError:
                    return HttpResponse(json.dumps({"Error": "pub_date not in required format YYYY-MM-DD"}),
                                        content_type='application/json')
                try:
                    retrieved_textbook.course = Course.objects.get(data['course_key'])
                except KeyError:
                    print("Course key was not sent in JSON request")
                except Course.DoesNotExist:
                    return HttpResponse(json.dumps({"Error": "Requested Course object does not exist"}),
                                        content_type='application/json')

                retrieved_textbook.save()

            except ValueError:  # Means that JSON was not a part of the request
                return HttpResponse(json.dumps({"Error": "JSON object not sent as part of POST request"}),
                                    content_type='application/json')

        response = {"status": "200", "textbook": retrieved_textbook.as_json()}
        return HttpResponse(json.dumps(response), content_type='application/json')

    except Textbook.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested Textbook object does not exist"}),
                            content_type='application/json')


@require_POST
def create_textbook(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        course_exists = False
        try:
            title = data['item_title']
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field item_title was not supplied"}),
                                content_type='application/json')
        try:
            author = data['item_author']
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field item_author was not supplied"}),
                                content_type='application/json')
        try:
            isbn = data['item_ISBN']
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field item_ISBN was not supplied"}),
                                content_type='application/json')
        try:
            date = data['pub_date']
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field pub_date was not supplied"}),
                                content_type='application/json')
        try:
            course = Course.objects.get(pk=data['course_key'])
            course_exists = True
        except KeyError:
            pass  # This is fine, since course is not required
        except Course.DoesNotExist:
            return HttpResponse(json.dumps({"Error": "Requested Course object does not exist"}),
                                content_type='application/json')
        try:
            if course_exists:
                new_textbook = Textbook.objects.create(item_title=title, item_author=author, item_ISBN=isbn,
                                                       pub_date=date, course=course)
            else:
                new_textbook = Textbook.objects.create(item_title=title, item_author=author, item_ISBN=isbn,
                                                       pub_date=date)
        except ValidationError:
            return HttpResponse(json.dumps({"Error": "pub_date not in required format YYYY-MM-DD"}),
                                content_type='application/json')

        response = {"status": "200", "new_textbook" : new_textbook.as_json()}
        return HttpResponse(json.dumps(response), content_type='application/json')  # Everything is a-ok

    except ValueError:  # Means that JSON was not a part of the request
        return HttpResponse(json.dumps({"Error": "JSON object not sent as part of POST request"}),
                            content_type='application/json')


@require_POST
def delete_textbook(request, pk):
    try:
        Textbook.objects.get(pk=pk).delete()
        return HttpResponse(json.dumps({"Status": "200"}))
    except Textbook.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested Textbook object does not exist"}),
                            content_type='application/json')


def details_listing(request, pk):
    pass


@require_POST
def create_listing(request):
    pass


@require_POST
def delete_listing(request, pk):
    try:
        Listing.objects.get(pk=pk).delete()
        return HttpResponse(json.dumps({"Status": "200"}))
    except Listing.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested Listing object does not exist"}),
                            content_type='application/json')
