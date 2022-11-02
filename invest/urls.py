from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.RedirectToSelfView.as_view()),
    path("users/<int:pk>/", views.InvestsView.as_view()),
]
