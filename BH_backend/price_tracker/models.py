from django.db import models
from scrapy_app.models import ProductSources

class PriceHistory(models.Model):
    product_source = models.ForeignKey(ProductSources, on_delete=models.CASCADE, related_name='price_history')
    price = models.CharField(max_length=100)
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_source.store_name} - {self.price} on {self.date_recorded}"
