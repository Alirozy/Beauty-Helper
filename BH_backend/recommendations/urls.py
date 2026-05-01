from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRecommendationViewSet, GenerateRecommendationView

router = DefaultRouter()
router.register(r'', UserRecommendationViewSet, basename='recommendation')

urlpatterns = [
    path('generate/', GenerateRecommendationView.as_view(), name='generate-recommendations'),
    path('', include(router.urls)),
]
