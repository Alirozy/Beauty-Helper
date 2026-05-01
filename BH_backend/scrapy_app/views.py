import subprocess
from pathlib import Path

from rest_framework import viewsets, filters, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
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


class TriggerScrapyCrawlView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        backend_root = Path(__file__).resolve().parents[2]
        project_root = backend_root.parent
        scrapy_root = project_root / "beauty_helper"

        if not scrapy_root.exists():
            return Response(
                {"detail": f"Scrapy project not found at: {scrapy_root}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            process = subprocess.Popen(
                ["scrapy", "crawl", "beauty_bot"],
                cwd=scrapy_root,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            return Response(
                {"detail": "Scrapy command not found. Install Scrapy in your environment."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as exc:
            return Response(
                {"detail": f"Failed to start crawler: {exc}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"message": "Crawler started.", "pid": process.pid},
            status=status.HTTP_202_ACCEPTED,
        )
