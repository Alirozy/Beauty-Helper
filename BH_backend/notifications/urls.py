from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PriceAlertViewSet

router = DefaultRouter()
router.register(r'', PriceAlertViewSet, basename='price-alert')

urlpatterns = [
    path('', include(router.urls)),
]
