from rest_framework import serializers
from .models import UserRecommendation
from scrapy_app.serializers import ProductSerializer

class UserRecommendationSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = UserRecommendation
        fields = ['id', 'user', 'product', 'product_details', 'reason', 'created_at']
        read_only_fields = ['user']
