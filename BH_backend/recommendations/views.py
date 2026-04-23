from rest_framework import viewsets, permissions
from .models import UserRecommendation
from .serializers import UserRecommendationSerializer

class UserRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserRecommendation.objects.filter(user=self.request.user).order_by('-created_at')
