from django.db import models
from users.models import CustomUser
from scrapy_app.models import Products

class PriceAlert(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='price_alerts')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='price_alerts')
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.user.username} on {self.product.name} at {self.target_price}"
