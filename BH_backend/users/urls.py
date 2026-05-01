from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import RegisterView, FavoriteViewSet, LoginView, LogoutView, DeleteAccountView, ProfileMeView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'favorites', FavoriteViewSet, basename='user-favorites')



urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('me/', ProfileMeView.as_view(), name='profile_me'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
    # Used to get a new token when the access token expires.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),


]





