from django.db import models
from django.contrib.auth.models import User
from extras.models import Address

class Order(models.Model):
    PENDING = "pending"
    SHIPPING = "shipping"
    DELIVERED = "delivered"
    ORDERSTATUS = (
        (PENDING, "Đang xử lý"),
        (SHIPPING, "Đang giao"),
        (DELIVERED, "Đã giao")
    )

    PAID = "trả"
    FAILED = "thất bại"
    PAYMENTSTATUS = (
        (PAID, "Trả"),
        (FAILED, "Thất bại"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    customer_id = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    order_products = models.JSONField(default=list)
    rated = models.JSONField(default=list)
    total_quantity = models.IntegerField()
    subtotal = models.IntegerField()
    total = models.IntegerField()
    delivery_status = models.CharField(max_length=255, choices=ORDERSTATUS, default=PENDING)
    payment_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} to {self.address.address}"
    


