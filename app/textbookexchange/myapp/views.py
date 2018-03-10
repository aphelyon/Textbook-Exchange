from django.shortcuts import render
from django.shortcuts import HttpResponse
from myapp.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from django.views.decorators.http import require_POST
import json
import datetime
from django.db import IntegrityError
from django.core.exceptions import ValidationError

# Create your views here.


def details_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        if request.method == "POST":
            try:
                data = json.loads(request.body.decode('utf-8'))
                try:
                    user.first_name = data['first_name']
                except KeyError:
                    print("first_name not sent in JSON POST request")  # This is not an error, we just don't do anything
                try:
                    user.last_name = data['last_name']
                except KeyError:
                    print("last_name not sent in JSON POST request")
                try:
                    user.username = data['username']
                except KeyError:
                    print("username not sent in JSON POST request")
                except IntegrityError:
                    return HttpResponse(json.dumps({"Error": "Username provided is already in use"}),
                                        content_type='application/json')
                try:
                    user.password = data['password']
                except KeyError:
                    print("password not sent in JSON POST request")
                try:
                    user.email = data['email']
                except KeyError:
                    print("email not sent in JSON POST request")
                except IntegrityError:
                    return HttpResponse(json.dumps({"Error": "Email provided is already in use"}),
                                        content_type='application/json')
                user.save()
            except ValueError:  # Means that JSON was not a part of the request
                return HttpResponse(json.dumps({"Error": "JSON object not sent as part of POST request"}),
                                    content_type='application/json')
        response = {"status": "200", "user": user.as_json()}
        return HttpResponse(json.dumps(response), content_type='application/json')
    except User.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested User object does not exist"}),
                            content_type='application/json')


@require_POST
def create_user(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        try:
            first_name = data['first_name']
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field first_name was not supplied"}),
                                content_type='application/json')
        try:
            last_name = data['last_name']
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field last_name was not supplied"}),
                                content_type='application/json')
        try:
            username = data['username']
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field username was not supplied"}),
                                content_type='application/json')
        try:
            password = data['password']
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field password was not supplied"}),
                                content_type='application/json')
        try:
            email = data['email']
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field email was not supplied"}),
                                content_type='application/json')
        except IntegrityError:
            return HttpResponse(json.dumps({"Error": "Email provided is already in use"}),
                                content_type='application/json')
        try:
            new_user = User.objects.create(first_name=first_name, last_name=last_name, username=username, password=password,
                                           email=email, userJoined=datetime.date.today())
        except IntegrityError as e:
            return HttpResponse(json.dumps({"Error": str(e)}),
                                content_type='application/json')
        response = {"status": "200", "User": new_user.as_json()}
        return HttpResponse(json.dumps(response), content_type='application/json')

    except ValueError:  # Means that JSON was not a part of the request
        return HttpResponse(json.dumps({"Error": "JSON object not sent as part of POST request"}),
                            content_type='application/json')


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
    try:
        retrieved_courses = Course.objects.get(pk=pk)
        if request.method == "POST":

            try:
                data = json.loads(request.body.decode('utf-8'))
                try:
                    retrieved_courses.identifier = data['identifier']
                except KeyError:
                    print("identifier was not sent in JSON request")
                try:
                    retrieved_courses.department = data['department']
                except KeyError:
                    print("department was not sent in JSON request")
                try:
                    retrieved_courses.name = data['name']
                except KeyError:
                    print("course_name was not sent in JSON request")
                except ValidationError:
                    return HttpResponse(json.dumps({"Error": ""}),
                                        content_type='application/json')
                try:
                    retrieved_courses.course = Course.objects.get(data['course_key'])
                except KeyError:
                    print("Course key was not sent in JSON request")
                except Course.DoesNotExist:
                    return HttpResponse(json.dumps({"Error": "Requested Course object does not exist"}),
                                        content_type='application/json')

                retrieved_courses.save()

            except ValueError:  # Means that JSON was not a part of the request
                return HttpResponse(json.dumps({"Error": "JSON object not sent as part of POST request"}),
                                    content_type='application/json')

        response = {"status": "200", "textbook": retrieved_courses.as_json()}
        return HttpResponse(json.dumps(response), content_type='application/json')

    except Course.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested Course object does not exist"}),
                            content_type='application/json')


@require_POST
def create_course(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        professor_exists = False
        try:
            identifier = data['identifier']
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field identifier was not supplied"}),
                                content_type='application/json')
        try:
            department = data['department']
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field department was not supplied"}),
                                content_type='application/json')
        try:
            name = data['name']
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field name was not supplied"}),
                                content_type='application/json')

        try:
            professor = Professor.objects.get(pk=data['professor_key'])
            professor_exists = True
        except KeyError:
            pass  # This is fine, since course is not required
        except Professor.DoesNotExist:
            return HttpResponse(json.dumps({"Error": "Requested Professor object does not exist"}),
                                content_type='application/json')
        try:
            if professor_exists:
                new_course = Course.objects.create(identifier=identifier, department=department,
                                                   name=name, professor=professor)
            else:
                new_course = Course.objects.create(identifier=identifier, department=department,
                                                   name=name)
        except ValidationError:
            return HttpResponse(json.dumps({"Error": "Something went wrong"}),
                                content_type='application/json')
        response = {"status": "200", "new_course": new_course.as_json()}
        return HttpResponse(json.dumps(response), content_type='application/json')  # Everything is a-ok

    except ValueError:  # Means that JSON was not a part of the request
        return HttpResponse(json.dumps({"Error": "JSON object not sent as part of POST request"}),
                            content_type='application/json')


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

        response = {"status": "200", "new_textbook": new_textbook.as_json()}
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


# We do not allow the listing's user to be changed, since a textbook listing will be posted by one user
def details_listing(request, pk):
    try:
        retrieved_listing = Listing.objects.get(pk=pk)
        if request.method == "POST":
            try:
                data = json.loads(request.body.decode('utf-8'))
                try:
                    retrieved_listing.item = Textbook.objects.get(pk=data['textbook_key'])
                except KeyError:
                    print("Textbook Key not sent")
                except Textbook.DoesNotExist:
                    return HttpResponse(json.dumps({"Error": "Requested Textbook object does not exist"}),
                                        content_type='application/json')
                try:
                    retrieved_listing.price_text = data['price']
                    retrieved_listing.actualprice = float(str(data['price']).replace(",", ""))
                except KeyError:
                    print("Price not sent")
                except ValueError:
                    return HttpResponse(json.dumps({"Error": "Price cannot be converted to a float"}),
                                        content_type='application/json')
                try:
                    # If the sent condition is a valid choice, set it, otherwise, don't
                    if data['condition'] in [item[0] for item in retrieved_listing.condition_of_textbook]:
                        retrieved_listing.condition = data['condition']
                    else:
                        condition_error = "Condition provided is not in list: " + str(retrieved_listing.condition_of_textbook)
                        return HttpResponse(json.dumps({"Error": condition_error}),
                                            content_type='application/json')
                except KeyError:
                    print("Textbook condition not sent")

                try:
                    # If the sent status is a valid choice, set it, otherwise, don't
                    if data['status'] in [item[0] for item in retrieved_listing.status_of_listing]:
                        retrieved_listing.status = data['status']
                    else:
                        status_error = "Status provided is not in list: " + str(retrieved_listing.status_of_listing)
                        return HttpResponse(json.dumps({"Error": status_error}),
                                            content_type='application/json')
                except KeyError:
                    print("Listing status not sent")

                retrieved_listing.save()
            except ValueError:
                return HttpResponse(json.dumps({"Error": "JSON object not sent as part of POST request"}),
                                    content_type='application/json')
        response = {"status": "200", "listing": retrieved_listing.as_json()}
        return HttpResponse(json.dumps(response), content_type='application/json')

    except Listing.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested Listing object does not exist"}),
                            content_type='application/json')


@require_POST
def create_listing(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        # We use this to handle our 3 cases all-in-one when a status isn't sent, a condition isn't sent, or both aren't
        argument_dictionary = {}
        try:
            argument_dictionary['item'] = Textbook.objects.get(pk=data['textbook_key'])
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field textbook_key was not supplied"}),
                                content_type='application/json')
        except Textbook.DoesNotExist:
            return HttpResponse(json.dumps({"Error": "Requested Textbook object does not exist"}),
                                content_type='application/json')
        try:
            argument_dictionary['price_text'] = data['price']
            argument_dictionary['actualprice'] = float(str(data['price']).replace(",", ""))
        except ValueError:
            return HttpResponse(json.dumps({"Error": "Price cannot be converted to a float"}),
                                content_type='application/json')
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field price was not supplied"}),
                                content_type='application/json')
        try:
            argument_dictionary['user'] = User.objects.get(pk=data['user_key'])
        except KeyError:
            return HttpResponse(json.dumps({"Error": "Required field user_key was not supplied"}),
                                content_type='application/json')
        except User.DoesNotExist:
            return HttpResponse(json.dumps({"Error": "Requested User object does not exist"}),
                                content_type='application/json')
        try:
            if data['condition'] in [item[0] for item in Listing.condition_of_textbook]:
                argument_dictionary['condition'] = data['condition']
            else:
                condition_error = "Condition provided is not in list: " + str(Listing.condition_of_textbook)
                return HttpResponse(json.dumps({"Error": condition_error}),
                                    content_type='application/json')
        except KeyError:
            pass  # Default value of 'NEW' will be used

        try:
            if data['status'] in [item[0] for item in Listing.status_of_listing]:
                argument_dictionary['status'] = data['status']
            else:
                status_error = "Status provided is not in list: " + str(Listing.status_of_listing)
                return HttpResponse(json.dumps({"Error": status_error}),
                                    content_type='application/json')
        except KeyError:
            pass  # Default value of 'For Sale' will be used

        new_listing = Listing.objects.create(**argument_dictionary)
        response = {"status": "200", "new_listing": new_listing.as_json()}
        return HttpResponse(json.dumps(response), content_type='application/json')  # Everything is a-ok

    except ValueError:  # Means that JSON was not a part of the request
        return HttpResponse(json.dumps({"Error": "JSON object not sent as part of POST request"}),
                            content_type='application/json')


@require_POST
def delete_listing(request, pk):
    try:
        Listing.objects.get(pk=pk).delete()
        return HttpResponse(json.dumps({"Status": "200"}))
    except Listing.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested Listing object does not exist"}),
                            content_type='application/json')


def user_listings(request, pk):
    """Retrieve a json-formatted list of all listings related to a user denoted by pk"""
    # We keep the list of listings here
    try:
        user = User.objects.get(pk=pk)
        user_listings = [listing.as_json() for listing in user.listing_set.all()]
        return HttpResponse(json.dumps(user_listings))
    except User.DoesNotExist:
        return HttpResponse(json.dumps({"Error": "Requested User object does not exist"}),
                            content_type='application/json')
