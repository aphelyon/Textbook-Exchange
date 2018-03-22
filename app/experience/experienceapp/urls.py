from django.conf.urls import url
from experienceapp import views

urlpatterns = []

urlpatterns += [url(r'^listings/(?P<pk>[-\w]+)$', views.listing_view, name='get-listing'),
                url(r'^listings$', views.Create_listing_view, name ='create_listing'),
                url(r'^get_all$', views.get_textbook_view, name='get_textbook'),
                url(r'^users/(?P<pk>[-\w]+)$', views.user_profile_view, name='get-user'),
                url(r'^courses/(?P<pk>[-\w]+)$', views.course_view, name='get-course'),
                url(r'^textbooks/(?P<pk>[-\w]+)$', views.textbook_view, name='get-textbook'),
                url(r'^home$', views.homepage_view, name='homepage-desktop'),
                url(r'^login$', views.login, name='login'),
                url(r'^logout$', views.logout, name='logout'),
                url(r'^signup$', views.signup, name='signup'),
                url(r'^navbar$', views.nav_bar, name='navbar')]
