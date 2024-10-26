from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("catalogue/", include("catalogue.urls")),
    path("transaction/", include("transaction.urls")),
    path("partner/", include("partner.urls")),
]
