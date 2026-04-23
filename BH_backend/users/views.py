from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

from .models import UserInteractions
from .serializers import FavoriteProductSerializer


class RegisterView(APIView):
    # Registration should be open to everyone, no authentication required
    permission_classes = [AllowAny]

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