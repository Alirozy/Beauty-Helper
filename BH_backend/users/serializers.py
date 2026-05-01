from rest_framework import serializers
from .models import CustomUser, UserProfile, UserPreferences, UserInteractions
from scrapy_app.serializers import ProductSerializer # The product serializer we wrote earlier
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }
        return data


class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_password(self, value):
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        if not user or not user.check_password(value):
            raise serializers.ValidationError("Password is incorrect.")

        return value


class UserProfileSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(source='profile.birth_date', allow_null=True, required=False)
    skin_type = serializers.CharField(source='profile.skin_type', allow_blank=True, allow_null=True, required=False)
    allergies = serializers.CharField(source='profile.allergies', allow_blank=True, allow_null=True, required=False)
    preferred_brands = serializers.CharField(
        source='preferences.preferred_brands', allow_blank=True, allow_null=True, required=False
    )
    preferred_product_types = serializers.CharField(
        source='preferences.preferred_product_types', allow_blank=True, allow_null=True, required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'birth_date',
            'skin_type',
            'allergies',
            'preferred_brands',
            'preferred_product_types',
        ]
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        preferences_data = validated_data.pop('preferences', {})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        profile, _ = UserProfile.objects.get_or_create(user=instance)
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        preferences, _ = UserPreferences.objects.get_or_create(user=instance)
        for attr, value in preferences_data.items():
            setattr(preferences, attr, value)
        preferences.save()

        return instance