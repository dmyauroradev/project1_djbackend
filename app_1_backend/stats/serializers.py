from rest_framework import serializers
from . import models


class SaleSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = models.Sale
        fields = ['product', 'quantity_sold', 'sale_date']


class RevenueStatsSerializer(serializers.Serializer):
    date = serializers.DateField()
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)

class UserGrowthStatsSerializer(serializers.Serializer):
    date = serializers.DateField()
    user_count = serializers.IntegerField()

class OrderStatsSerializer(serializers.Serializer):
    date = serializers.DateField()
    order_count = serializers.IntegerField()

class BestSellingProductsSerializer(serializers.Serializer):
    product__title = serializers.CharField(max_length=255)
    total_quantity_sold = serializers.IntegerField()

class TopUsersByOrdersSerializer(serializers.Serializer):
    month = serializers.DateField()
    username = serializers.CharField()
    total_orders = serializers.IntegerField()