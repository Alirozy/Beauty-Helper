from rest_framework import serializers
from .models import PriceAlert

class PriceAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceAlert
        fields = ['id', 'user', 'product', 'target_price', 'is_active', 'created_at']
        read_only_fields = ['user']
