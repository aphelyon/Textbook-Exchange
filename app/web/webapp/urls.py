from django.conf.urls import url
from webapp import views


urlpatterns = [url(r'^home$', views.index, name='index'),
               url(r'^listing/(?P<pk>\d+)$', views.listing_view, name='listing'),]
