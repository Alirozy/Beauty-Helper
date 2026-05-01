from django.db import models
from django.contrib.auth.models import AbstractUser
from scrapy_app.models import Brands, Products, ProductSources

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) # blank ve null default zaten yönetilir
    phone_number = models.CharField(unique=True, max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(blank=True, null=True)
    skin_type = models.CharField(max_length=50, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)

    def __str__(self):
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return full_name or self.user.username

class UserPreferences(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='preferences')
    preferred_brands = models.TextField(blank=True, null=True)
    preferred_product_types = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Preferences of {self.user.username}"
        
class UserInteractions(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interactions')
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    interaction_type = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True) # Zamanı otomatik kaydeder

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type}"