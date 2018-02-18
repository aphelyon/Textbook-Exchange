from django.conf.urls import url
from myapp import views

urlpatterns = []

urlpatterns += [
    url(r'^v1/users/(?P<pk>[-\w]+)/delete$', views.delete_user, name='delete-user-api'),
]

urlpatterns += [
    url(r'^v1/courses/(?P<pk>[-\w]+)/delete$', views.delete_user, name='delete-course-api'),
]

urlpatterns += [
    url(r'^v1/professors/create$', views.create_professor, name='create-new-professor-api'),  # Keep this on top, please
    url(r'^v1/professors/(?P<pk>[-\w]+)$', views.details_professor, name='get-professor-api'),
    url(r'^v1/professors/(?P<pk>[-\w]+)/delete$', views.delete_professor, name='delete-professor-api'),
]

urlpatterns += [
    url(r'^v1/textbooks/create$', views.create_textbook, name='create-textbook-api'),  # Keep this on top, please
    url(r'^v1/textbooks/(?P<pk>[-\w]+)$', views.details_textbook, name='get-textbook-api'),
    url(r'^v1/textbooks/(?P<pk>[-\w]+)/delete$', views.delete_textbook, name='delete-textbook-api'),
]

urlpatterns += [
    url(r'^v1/listings/(?P<pk>[-\w]+)/delete$', views.delete_listing, name='delete-listing-api'),
]
