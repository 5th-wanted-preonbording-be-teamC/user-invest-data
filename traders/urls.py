from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/<str:number>/", views.DepositAndWithdrawal.as_view()),
    path("", views.TraderList.as_view()),
]
