from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet, OrderProductViewSet, UserFavoriteProductViewSet

router = routers.DefaultRouter()
router.register(r'phoneproducts', ProductViewSet)
router.register(r'phone-order-products', OrderProductViewSet)
router.register(r'phone-favorite-products', UserFavoriteProductViewSet)


# router.register(r'',)


urlpatterns = [
    path('', include(router.urls))
]
