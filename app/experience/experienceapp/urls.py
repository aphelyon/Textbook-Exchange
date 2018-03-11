from django.conf.urls import url
from experienceapp import views

urlpatterns = []

urlpatterns += [url(r'^listings/(?P<pk>[-\w]+)$', views.listing_view, name='get-listing'),
                url(r'^home$', views.homepage_view, name='homepage-desktop')]
