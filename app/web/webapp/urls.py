from django.conf.urls import url
from webapp import views


urlpatterns = [url(r'^$', views.index, name='index'),
               url(r'^login$', views.login, name='login'),
               url(r'^logout$', views.logout, name='logout'),
               url(r'^signup$', views.signup, name='signup'),
               url(r'^listing/(?P<pk>\d+)$', views.listing_view, name='listing'),
               url(r'^listing$', views.Create_listing_view, name = 'create_listing'),
               url(r'^search$', views.search_view, name = 'search'),
               url(r'^user/(?P<pk>\d+)$', views.user_profile_view, name='user'),
               url(r'^course/(?P<pk>\d+)$', views.course_view, name='course'),
               url(r'^course$', views.create_course_view, name='create_course'),
               url(r'^professor$', views.create_professor_view, name='create_professor'),
               url(r'^textbook/(?P<pk>\d+)$', views.textbook_view, name='textbook'),
               url(r'^textbook$', views.create_textbook_view, name='create_textbook'),]
