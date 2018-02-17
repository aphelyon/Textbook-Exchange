from django.conf.urls import url
from myapp import views

urlpatterns = [
    url(r'^v1/professors/(?P<pk>[-\w]+)/$', views.details_professor, name='get-professor-api'),
    url(r'^v1/professors/create/$', views.create_professor, name='create-new-professor-api'),
    url(r'^v1/professors/(?P<pk>[-\w]+)/delete/$', views.delete_professor, name='delete-professor-api')
]