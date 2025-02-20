from rest_framework import routers

from products.apps import ProductsConfig
from products.views import ProductsViewSet

app_name = ProductsConfig.name

router = routers.DefaultRouter()
router.register("", ProductsViewSet, basename="products")

urlpatterns = router.urls
