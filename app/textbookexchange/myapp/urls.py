from django.conf.urls import url
from myapp import views

urlpatterns = [
    url(r'^v1/professors/create/$', views.create_professor, name='create-new-professor-api')
]
