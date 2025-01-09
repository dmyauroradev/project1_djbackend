from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from core.models import Product 

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    sale_date = models.DateTimeField(default=timezone.now, blank=False)

    def __str__(self):
        return f'{self.product.title} - Sold {self.quantity_sold} on {self.sale_date}'

