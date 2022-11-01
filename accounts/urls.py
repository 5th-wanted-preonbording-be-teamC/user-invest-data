from django.urls import path
from . import views


urlpatterns = [
    path("", views.AccountsView.as_view()),
]
