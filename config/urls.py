from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from store.api import CategoryViewSet, ProductViewSet, OrderViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="api-category")
router.register("products", ProductViewSet, basename="api-product")
router.register("orders", OrderViewSet, basename="api-order")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("", include("store.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
