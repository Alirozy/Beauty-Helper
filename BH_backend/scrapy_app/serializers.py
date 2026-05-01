from rest_framework import serializers
from .models import Products, Brands, ProductSources

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ['id', 'brand', 'website']

class ProductSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSources
        fields = ['id', 'store_name', 'store_url', 'price', 'currency', 'stock']

class ProductSerializer(serializers.ModelSerializer):
    # To include brand and sources details in the JSON response:
    brand = BrandSerializer(read_only=True)
    sources = ProductSourceSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = ['id', 'name', 'brand', 'type', 'description', 'production_year', 'poster_url', 'rating', 'sources']