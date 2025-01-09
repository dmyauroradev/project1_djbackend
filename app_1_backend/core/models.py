from django.db import models
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    imageUrl = models.URLField(blank=False)

    def __str__(self) -> str:
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    decorationType = models.CharField(max_length=100, default="None")
    ratings = models.FloatField(blank=False, default=1.0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    code = models.JSONField(blank=True)
    dimensions = models.JSONField(blank=True)
    imageUrls = models.JSONField(blank=True)
    stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    #brand = models.CharField(max_length=100)
    #material = models.CharField(max_length=150)
    #ecoFriendlyLevel = models.FloatField(blank=False, default=1.0)
    #applications = models.CharField(max_length=200, default='None')
    #style = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title