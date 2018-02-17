from django.shortcuts import render
from django.shortcuts import HttpResponse
from myapp.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.


def create_professor(request):
    if request.method == "POST":
        newProfessor = Professor.objects.create(name=request.POST.get("name"), email=request.POST.get("email"))
        return HttpResponse(newProfessor.as_json(), content_type='application/json')
    else:
        response = render_to_response('404.html', {},
                                      context_instance=RequestContext(request))
        response.status_code = 404
        return response