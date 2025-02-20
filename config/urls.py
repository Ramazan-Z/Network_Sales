from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Administrative panel
    path("admin/", admin.site.urls, name="admin"),
    # Documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    # User authentication
    path("users/login/", TokenObtainPairView.as_view(), name="user-login"),
    path("users/refresh_token/", TokenRefreshView.as_view(), name="refresh-token"),
    # Products
    path("products/", include("products.urls", namespace="products")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
