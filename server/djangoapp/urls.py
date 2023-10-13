"""this file defines URL patterns for djangoapp"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route = 'djangoapp/about', view = views.about, name='about'),
    # path for contact us view
    path(route = 'djangoapp/contact', view = views.contact, name='contact'),
    # path for registration
    path("registration/", views.registration_request, name="registration"),
    # path for login
    path("login/", views.login_request, name="login"),
    # path for logout
    path("logout/", views.logout_request, name="logout"),
    # path for get dealership view
    path(route='', view=views.get_dealerships, name='index'),
    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    # path for add a review view
    path('add_review/<int:dealer_id>/', views.add_review, name='add_review'),
    
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
