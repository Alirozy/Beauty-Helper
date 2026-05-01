from django.db import models

# Create your models here.
class Brands(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.CharField(unique=True, max_length=255)
    website = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brands'

class Products(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(Brands, models.DO_NOTHING, db_column='brand_id', blank=True, null=True)
    name = models.CharField(unique=True, max_length=500)
    type = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    production_year = models.CharField(max_length=50, blank=True, null=True)
    poster_url = models.TextField(blank=True, null=True)
    rating = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'

class ProductSources(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Products,
        models.DO_NOTHING,
        db_column='product_id',
        blank=True,
        null=True,
        related_name='sources',
    )
    store_name = models.CharField(max_length=255, blank=True, null=True)
    store_url = models.TextField(unique=True, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=50, blank=True, null=True)
    stock = models.CharField(max_length=50, blank=True, null=True, db_column='stock')

    class Meta:
        managed = False
        db_table = 'product_sources'