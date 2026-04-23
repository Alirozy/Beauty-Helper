from django.db import models
from users.models import CustomUser
from scrapy_app.models import Products

class UserRecommendation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recommendations')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='recommended_for')
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.product.name}"
