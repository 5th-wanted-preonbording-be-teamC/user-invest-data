from django.urls import path
from . import views

urlpatterns = [
    path("user/", views.RedirectToSelfView.as_view()),
    path("user/<int:user_pk>/", views.InvestsView.as_view()),
    path(
        "user/<int:user_pk>/account/<int:account_pk>/", views.InvestDetailView.as_view()
    ),
    path(
        "user/<int:user_pk>/account/<int:account_pk>/assets/",
        views.InvestTransactionsView.as_view(),
    ),
]
