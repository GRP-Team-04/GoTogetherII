""" This file is used to define url pattern for users application """

from django.conf.urls import url
from django.contrib.auth.views import LoginView

from . import views

app_name = "users"

urlpatterns = [
    # Log in page
    url(r'^login/$', LoginView.as_view(template_name='users/login.html'), name = 'login'),
    
    # Log out page
    url(r'^logout/$', views.logout_view, name='logout'),

    # Register page
    url(r'^register/$', views.register, name='register'),

]

