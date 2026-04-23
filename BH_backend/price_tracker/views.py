from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import PriceHistory
from .serializers import PriceHistorySerializer

class PriceHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PriceHistory.objects.all().order_by('-date_recorded')
    serializer_class = PriceHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_source', 'product_source__product']
