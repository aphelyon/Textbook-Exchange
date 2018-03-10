from django.conf.urls import url
from webapp import views


urlpatterns = [url(r'^home$', views.index, name='index'),]