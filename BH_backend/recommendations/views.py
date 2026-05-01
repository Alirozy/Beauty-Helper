from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserRecommendation
from .serializers import UserRecommendationSerializer
from .services import generate_rule_based_recommendations

class UserRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserRecommendation.objects.filter(user=self.request.user).order_by('-created_at')


class GenerateRecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        limit = request.data.get("limit", 10)
        try:
            limit = max(1, min(int(limit), 50))
        except (TypeError, ValueError):
            return Response(
                {"detail": "limit must be an integer between 1 and 50."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        recommendations = generate_rule_based_recommendations(request.user, limit=limit)
        serializer = UserRecommendationSerializer(recommendations, many=True)
        return Response(
            {
                "message": "Rule-based recommendations generated.",
                "count": len(serializer.data),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
