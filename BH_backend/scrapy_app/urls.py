from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, TriggerScrapyCrawlView

router = DefaultRouter()
router.register(r'list', ProductViewSet, basename='product')

urlpatterns = [
    path('crawl/', TriggerScrapyCrawlView.as_view(), name='scrapy-crawl'),
    path('', include(router.urls)),
]
