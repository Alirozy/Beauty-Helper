from rest_framework import serializers
from .models import CustomUser, UserProfile, UserPreferences, UserInteractions
from scrapy_app.serializers import ProductSerializer # The product serializer we wrote earlier


class RegisterSerializer(serializers.ModelSerializer):
    # Fields that are not in the database but are required for validation
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirm', 'phone_number']

    # Custom method to check if passwords match
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        # We delete the password_confirm field before sending it to the database
        validated_data.pop('password_confirm')
        
        # Secure user creation (Password hashing is done here)
        user = CustomUser.objects.create_user(**validated_data)
        return user


class FavoriteProductSerializer(serializers.ModelSerializer):
    # To see the product details completely
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = UserInteractions
        fields = ['id', 'product', 'product_details', 'timestamp']