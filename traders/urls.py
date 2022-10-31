
from django.urls import path

from traders import views

urlpatterns = [
    path("", views.TradersView.as_view()),
]
