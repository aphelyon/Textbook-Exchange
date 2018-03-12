from django.conf.urls import url
from webapp import views


urlpatterns = [url(r'^home$', views.index, name='index'),
               url(r'^listing/(?P<pk>\d+)$', views.listing_view, name='listing'),
               url(r'^user/(?P<pk>\d+)$', views.user_profile_view, name='user'),]
