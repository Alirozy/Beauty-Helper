from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import PriceAlert
from .serializers import PriceAlertSerializer

class PriceAlertViewSet(viewsets.ModelViewSet):
    serializer_class = PriceAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'is_active']

    def get_queryset(self):
        return PriceAlert.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
