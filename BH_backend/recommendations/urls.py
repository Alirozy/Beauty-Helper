from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRecommendationViewSet

router = DefaultRouter()
router.register(r'', UserRecommendationViewSet, basename='recommendation')

urlpatterns = [
    path('', include(router.urls)),
]
