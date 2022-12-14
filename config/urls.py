from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/assets/", include("assets.urls")),
    path("api/v1/transactions/", include("transactions.urls")),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/invest/", include("invest.urls")),
]
