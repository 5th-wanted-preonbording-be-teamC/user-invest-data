from django.urls import path
from . import views

urlpatterns = [
    path("", views.TransactionsView.as_view()),
]
