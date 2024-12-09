from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from catalogue.views import homepage_view

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("catalogue/", include("catalogue.urls")),
                  path("transaction/", include("transaction.urls")),
                  path("partner/", include("partner.urls")),
                  path("cart/", include("cart.urls")),
                  path('', homepage_view, name='homepage')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
