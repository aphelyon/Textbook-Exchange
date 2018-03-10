from django.conf.urls import url
from myapp import views

urlpatterns = []

urlpatterns += [
    url(r'^v1/users/create$', views.create_user, name='create-user-api'),  # Keep this on top, please
    url(r'^v1/users/(?P<pk>[-\w]+)$', views.details_user, name='get-user-api'),
    url(r'^v1/users/(?P<pk>[-\w]+)/delete$', views.delete_user, name='delete-user-api'),
]

urlpatterns += [
    url(r'^v1/courses/create$', views.create_course, name='create-new-course-api'),  # Keep this on top, please
    url(r'^v1/courses/(?P<pk>[-\w]+)$', views.details_course, name='get-course-api'),
    url(r'^v1/courses/(?P<pk>[-\w]+)/delete$', views.delete_course, name='delete-course-api'),
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
    url(r'^v1/listings/create$', views.create_listing, name='create-listing-api'),  # Keep this on top, please
    url(r'^v1/listings/from_user/(?P<pk>[-\w]+)$', views.user_listings, name='get-user-listings'),
    url(r'^v1/listings/(?P<pk>[-\w]+)$', views.details_listing, name='get-listing-api'),
    url(r'^v1/listings/(?P<pk>[-\w]+)/delete$', views.delete_listing, name='delete-listing-api'),
]
