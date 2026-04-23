from rest_framework import serializers
from .models import PriceHistory

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['id', 'product_source', 'price', 'date_recorded']
