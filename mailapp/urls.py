from django.urls import path
from . import views
""" This file defines the URL patterns for the mailapp application. It maps specific URL paths to corresponding view 
functions that handle the logic for each route. The urlpatterns list includes paths for the login page, home page, 
email history page, and registration page. Each path is associated with a view function that processes the request 
and returns an appropriate response, such as rendering a template or redirecting to another page. This setup allows 
users to navigate through different sections of the application based on the defined routes. """

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('history/', views.history,  name='history'),
    path('register/', views.register, name='register'),
]