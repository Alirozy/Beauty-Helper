from rest_framework import status, viewsets, permissions, throttling
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import RegisterSerializer, LoginSerializer, DeleteAccountSerializer, UserProfileSerializer

from .models import UserInteractions
from .serializers import FavoriteProductSerializer


class RegisterView(APIView):
    # Registration should be open to everyone, no authentication required
    permission_classes = [AllowAny]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = 'auth'

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully.",
                "user": {
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)
        
        # If there is a validation error (e.g. passwords don't match), return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only the "favorite" interactions of the currently logged-in user
        return UserInteractions.objects.filter(
            user=self.request.user, 
            interaction_type='favorite'
        )

    def perform_create(self, serializer):
        # Automatically set the user as the logged-in user when adding a favorite
        serializer.save(user=self.request.user, interaction_type='favorite')


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = 'auth'


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except AttributeError:
            return Response(
                {
                    "detail": "Token blacklist is not enabled. Add 'rest_framework_simplejwt.token_blacklist' to INSTALLED_APPS."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)


class DeleteAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        serializer = DeleteAccountSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        request.user.delete()
        return Response({"message": "Account deleted successfully."}, status=status.HTTP_200_OK)


class ProfileMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)