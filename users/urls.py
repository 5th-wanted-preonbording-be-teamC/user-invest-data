from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("login", views.Login.as_view()),
    path("logout", views.Users.as_view()),
]
