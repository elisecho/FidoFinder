from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = 'users'
urlpatterns = [
    #Login page.
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    #logout page.
    path('logged_out/', LogoutView.as_view(template_name='users/logged_out.html'), name='logged_out'),
    #registration page.
    path('register/', views.register, name='register'),
]