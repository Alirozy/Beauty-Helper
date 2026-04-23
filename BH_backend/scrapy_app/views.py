from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Products
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows products to be viewed and searched.
    ReadOnlyModelViewSet provides default 'list' and 'retrieve' actions.
    """
    queryset = Products.objects.all().order_by('id')
    serializer_class = ProductSerializer
    
    # Enable filtering and searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
    # Fields that can be filtered exactly
    filterset_fields = ['brand__brand', 'type', 'production_year', 'rating']
    
    # Fields that can be searched using partial text
    search_fields = ['name', 'description']
