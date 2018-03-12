from django.shortcuts import render
from django.http import JsonResponse
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


def error(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})

def success(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'results': resp})
    else:
        return JsonResponse({'ok': True})

def details_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        if request.method == "POST":
            try:
                data = request.POST
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
                    return error(request, "Username provided is already in use")
                try:
                    user.password = data['password']
                except KeyError:
                    print("password not sent in JSON POST request")
                try:
                    user.email = data['email']
                except KeyError:
                    print("email not sent in JSON POST request")
                except IntegrityError:
                    return error(request, "Email provided is already in use")
                user.save()
            except ValueError:  # Means that JSON was not a part of the request
                return error("JSON object not sent as part of POST request")
        response = user.as_json()
        return success(request, response)
    except User.DoesNotExist:
        return error(request, "Requested User object does not exist")


@require_POST
def create_user(request):
    try:
        data = request.POST
        try:
            first_name = data['first_name']
        except KeyError:
            return error(request, "Required field first_name was not supplied")
        try:
            last_name = data['last_name']
        except KeyError:
            return error(request, "Required field last_name was not supplied")
        try:
            username = data['username']
        except KeyError:
            return error(request, "Required field username was not supplied")
        try:
            password = data['password']
        except KeyError:
            return error(request, "Required field password was not supplied")
        try:
            email = data['email']
        except KeyError:
            return error(request, "Required field email was not supplied")
        except IntegrityError:
            return error(request, "Email provided is already in use")
        try:
            new_user = User.objects.create(first_name=first_name, last_name=last_name, username=username, password=password,
                                           email=email, userJoined=datetime.date.today())
        except IntegrityError as e:
            return error(request, str(e))
        response = {"Status": "200", "User": new_user.as_json()}
        return success(request, response)
    except ValueError:
        return error(request, "JSON object not sent as part of POST request")

@require_POST
def delete_user(request, pk):
    try:
        User.objects.get(pk=pk).delete()
        return success(request, {"Status": "200"})
    except User.DoesNotExist:
        return error(request, "Requested User object does not exist")


# This method is for getting a professor's details and or updating them. I couldn't think of a better name to encompass
# both things
def details_professor(request, pk):
    try:
        retrieved_professor = Professor.objects.get(pk=pk)

        if request.method == "POST":
            try:
                data = request.POST
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
                return error(request, "JSON object not sent as part of POST request")

        response = retrieved_professor.as_json()
        return success(request, response)

    except Professor.DoesNotExist:
        return error(request, "Requested Professor object does not exist")

@require_POST
def create_professor(request):
    try:
        data = request.POST
        try:
            name = data['name']
        except KeyError:
            return error(request, "Required field name was not supplied")
        try:
            email = data['email']
        except KeyError: # Email is not a required field
            new_professor = Professor.objects.create(name=name)
        else:
            new_professor = Professor.objects.create(name=name, email=email)

        response = new_professor.as_json()
        return success(request, response)

    except ValueError:  # Means that JSON was not a part of the request
        return error(request, "JSON object not sent as part of POST request")


@require_POST
def delete_professor(request, pk):
    try:
        Professor.objects.get(pk=pk).delete()
        return success(request, {"Status": "200"})
    except Professor.DoesNotExist:
        return error(request, "Requested Professor object does not exist")


def details_course(request, pk):
    try:
        retrieved_courses = Course.objects.get(pk=pk)
        if request.method == "POST":

            try:
                data = request.POST
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
                    return error(request, "JSON object not sent as part of POST request")
                try:
                    retrieved_courses.course = Course.objects.get(data['course_key'])
                except KeyError:
                    print("Course key was not sent in JSON request")
                except Course.DoesNotExist:
                    return error(request, "Requested Course object does not exist")

                retrieved_courses.save()

            except ValueError:  # Means that JSON was not a part of the request
                return error(request, "JSON object not sent as part of POST request")

        response = retrieved_courses.as_json()
        return success(request, response)

    except Course.DoesNotExist:
        return error(request, "Requested Course object does not exist")


@require_POST
def create_course(request):
    try:
        data = request.POST
        professor_exists = False
        try:
            identifier = data['identifier']
        except KeyError:
            return error(request, "Required field identifier was not supplied")
        try:
            department = data['department']
        except KeyError:
            return error(request, "Required field department was not supplied")
        try:
            name = data['name']
        except KeyError:
            return error(request, "Required field name was not supplied")

        try:
            professor = Professor.objects.get(pk=data['professor_key'])
            professor_exists = True
        except KeyError:
            pass  # This is fine, since course is not required
        except Professor.DoesNotExist:
            return error(request, "Requested Professor object does not exist")
        try:
            if professor_exists:
                new_course = Course.objects.create(identifier=identifier, department=department,
                                                   name=name, professor=professor)
            else:
                new_course = Course.objects.create(identifier=identifier, department=department,
                                                   name=name)
        except ValidationError:
            return error(request, "Something went wrong")
        response = new_course.as_json()
        return success(request, response)  # Everything is a-ok

    except ValueError:  # Means that JSON was not a part of the request
        return error(request, "JSON object not sent as part of POST request")


@require_POST
def delete_course(request, pk):
    try:
        Course.objects.get(pk=pk).delete()
        return success(request, {"Status": "200"})
    except Course.DoesNotExist:
        return error(request, "Requested Course object does not exist")

def details_textbook(request, pk):
    try:
        retrieved_textbook = Textbook.objects.get(pk=pk)
        if request.method == "POST":

            try:
                data = request.POST
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
                    return error(request, "pub_date not in required format YYYY-MM-DD")
                try:
                    retrieved_textbook.course = Course.objects.get(data['course_key'])
                except KeyError:
                    print("Course key was not sent in JSON request")
                except Course.DoesNotExist:
                    return error(request, "Requested Course object does not exist")

                retrieved_textbook.save()

            except ValueError:  # Means that JSON was not a part of the request
                return error(request, "JSON object not sent as part of POST request")

        response = retrieved_textbook.as_json()
        return success(request, response)

    except Textbook.DoesNotExist:
        return error(request, "Requested Textbook object does not exist")

@require_POST
def create_textbook(request):
    try:
        data = request.POST
        course_exists = False
        try:
            title = data['item_title']
        except KeyError:
            return error(request, "Required field item_title was not supplied")
        try:
            author = data['item_author']
        except KeyError:
            return error(request, "Required field item_author was not supplied")
        try:
            isbn = data['item_ISBN']
        except KeyError:
            return error(request, "Required field item_ISBN was not supplied")
        try:
            date = data['pub_date']
        except KeyError:
            return error(request, "Required field pub_date was not supplied")
        try:
            course = Course.objects.get(pk=data['course_key'])
            course_exists = True
        except KeyError:
            pass  # This is fine, since course is not required
        except Course.DoesNotExist:
            return error(request, "Requested Course object does not exist")
        try:
            if course_exists:
                new_textbook = Textbook.objects.create(item_title=title, item_author=author, item_ISBN=isbn,
                                                       pub_date=date, course=course)
            else:
                new_textbook = Textbook.objects.create(item_title=title, item_author=author, item_ISBN=isbn,
                                                       pub_date=date)
        except ValidationError:
            return error(request, "pub_date not in required format YYYY-MM-DD")

        response = new_textbook.as_json()
        return success(request, response)  # Everything is a-ok

    except ValueError:  # Means that JSON was not a part of the request
        return error(request, "JSON object not sent as part of POST request")


@require_POST
def delete_textbook(request, pk):
    try:
        Textbook.objects.get(pk=pk).delete()
        return success(request, {"Status": "200"})
    except Textbook.DoesNotExist:
        return error(request, "Requested Textbook object does not exist")


# We do not allow the listing's user to be changed, since a textbook listing will be posted by one user
def details_listing(request, pk):
    try:
        retrieved_listing = Listing.objects.get(pk=pk)
        if request.method == "POST":
            try:
                data = request.POST
                try:
                    retrieved_listing.item = Textbook.objects.get(pk=data['textbook_key'])
                except KeyError:
                    print("Textbook Key not sent")
                except Textbook.DoesNotExist:
                    return error(request, "Requested Textbook object does not exist")
                try:
                    retrieved_listing.price_text = data['price']
                    retrieved_listing.actualprice = float(str(data['price']).replace(",", ""))
                except KeyError:
                    print("Price not sent")
                except ValueError:
                    return error(request, "Price cannot be converted to a float")
                try:
                    # If the sent condition is a valid choice, set it, otherwise, don't
                    if data['condition'] in [item[0] for item in retrieved_listing.condition_of_textbook]:
                        retrieved_listing.condition = data['condition']
                    else:
                        condition_error = "Condition provided is not in list: " + str(retrieved_listing.condition_of_textbook)
                        return error(request, condition_error)
                except KeyError:
                    print("Textbook condition not sent")

                try:
                    # If the sent status is a valid choice, set it, otherwise, don't
                    if data['status'] in [item[0] for item in retrieved_listing.status_of_listing]:
                        retrieved_listing.status = data['status']
                    else:
                        status_error = "Status provided is not in list: " + str(retrieved_listing.status_of_listing)
                        return error(request, status_error)
                except KeyError:
                    print("Listing status not sent")

                retrieved_listing.save()
            except ValueError:
                return error(request, "JSON object not sent as part of POST request")
        response = retrieved_listing.as_json()
        return success(request, response)

    except Listing.DoesNotExist:
        return error(request, "Requested Listing object does not exist")


@require_POST
def create_listing(request):
    try:
        data = request.POST
        # We use this to handle our 3 cases all-in-one when a status isn't sent, a condition isn't sent, or both aren't
        argument_dictionary = {}
        try:
            argument_dictionary['item'] = Textbook.objects.get(pk=data['textbook_key'])
        except KeyError:
            return error(request, "Required field textbook_key was not supplied")
        except Textbook.DoesNotExist:
            return error(request, "Requested Textbook object does not exist")
        try:
            argument_dictionary['price_text'] = data['price']
            argument_dictionary['actualprice'] = float(str(data['price']).replace(",", ""))
        except ValueError:
            return error(request, "Price cannot be converted to a float")
        except KeyError:
            return error(request, "Required field price was not supplied")
        try:
            argument_dictionary['user'] = User.objects.get(pk=data['user_key'])
        except KeyError:
            return error(request, "Required field user_key was not supplied")
        except User.DoesNotExist:
            return error(request, "Requested User object does not exist")
        try:
            if data['condition'] in [item[0] for item in Listing.condition_of_textbook]:
                argument_dictionary['condition'] = data['condition']
            else:
                condition_error = "Condition provided is not in list: " + str(Listing.condition_of_textbook)
                return error(request, condition_error)
        except KeyError:
            pass  # Default value of 'NEW' will be used

        try:
            if data['status'] in [item[0] for item in Listing.status_of_listing]:
                argument_dictionary['status'] = data['status']
            else:
                status_error = "Status provided is not in list: " + str(Listing.status_of_listing)
                return error(request, status_error)
        except KeyError:
            pass  # Default value of 'For Sale' will be used
        argument_dictionary['time_created'] = datetime.datetime.now()

        new_listing = Listing.objects.create(**argument_dictionary)
        response = new_listing.as_json()
        return success(request, response)  # Everything is a-ok

    except ValueError:  # Means that JSON was not a part of the request
        return error(request, "JSON object not sent as part of POST request")


@require_POST
def delete_listing(request, pk):
    try:
        Listing.objects.get(pk=pk).delete()
        return success(request, {"Status": "200"})
    except Listing.DoesNotExist:
        return error(request, "Requested Listing object does not exist")


def user_listings(request, pk):
    """Retrieve a json-formatted list of all listings related to a user denoted by pk"""
    # We keep the list of listings here
    try:
        user = User.objects.get(pk=pk)
        user_listings = [listing.as_json() for listing in user.listing_set.all()]
        return success(request, user_listings)
    except User.DoesNotExist:
        return error(request, "Requested User object does not exist")


def view_count_listings(request, pk):
    """Update the view count of a particular listing"""
    try:
        listing = Listing.objects.get(pk=pk)
        listing.viewed_count += 1
        listing.save()
        return success(request)
    except Listing.DoesNotExist:
        return error(request, "Requested Listing object does not exist")


def most_viewed_listings(request):
    most_viewed_queryset = Listing.objects.order_by('-viewed_count')
    if len(most_viewed_queryset) < 5:
        most_viewed = [listing.as_json() for listing in most_viewed_queryset]
    else:
        most_viewed = [listing.as_json() for listing in most_viewed_queryset[:5]]
    if len(most_viewed) > 0:
        return success(request, most_viewed)
    else:
        return error(request, "No Listing objects exist")


def newest_listings(request):
    newest_queryset = Listing.objects.order_by('-time_created')
    if len(newest_queryset) < 5:
        newest = [listing.as_json() for listing in newest_queryset]
    else:
        newest = [listing.as_json() for listing in newest_queryset[:5]]
    if len(newest) > 0:
        return success(request, newest)
    else:
        return error(request, "No Listing objects exist")
