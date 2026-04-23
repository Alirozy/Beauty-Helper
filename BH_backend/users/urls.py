from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
        TokenRefreshView,
)
from .views import RegisterView
from rest_framework.routers import DefaultRouter
from .views import FavoriteViewSet

router = DefaultRouter()
router.register(r'favorites', FavoriteViewSet, basename='user-favorites')



urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Used to get a new token when the access token expires.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),


]





