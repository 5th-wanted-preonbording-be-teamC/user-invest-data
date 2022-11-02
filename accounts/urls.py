from django.urls import path
from . import views


urlpatterns = [
    path("", views.AccountsView.as_view()),
    path("transfer/", views.AccountTransferView.as_view()),
]
