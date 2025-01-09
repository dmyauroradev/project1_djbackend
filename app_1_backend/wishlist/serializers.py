from rest_framework import serializers
from . import models

class WishListSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    title = serializers.ReadOnlyField(source='product.title')
    description = serializers.ReadOnlyField(source='product.description')
    is_featured = serializers.ReadOnlyField(source='product.is_featured')
    decorationType = serializers.ReadOnlyField(source='product.decorationType')
    price = serializers.ReadOnlyField(source='product.price')
    ratings = serializers.ReadOnlyField(source='product.ratings')
    category = serializers.ReadOnlyField(source='product.category.id')
    brand = serializers.ReadOnlyField(source='product.brand')
    material = serializers.ReadOnlyField(source='product.material')
    ecoFriendlyLevel = serializers.ReadOnlyField(source='product.ecoFriendlyLevel')
    code = serializers.ReadOnlyField(source='product.code')
    dimensions = serializers.ReadOnlyField(source='product.dimensions')
    applications = serializers.ReadOnlyField(source='product.applications')
    style = serializers.ReadOnlyField(source='product.style')
    imageUrls = serializers.ReadOnlyField(source='product.imageUrls')
    stock_quantity = serializers.ReadOnlyField(source='product.stock_quantity')
    created_at = serializers.ReadOnlyField(source='product.created_at')

    class Meta:
        model = models.WishList
        fields = ['id','title','description','price','is_featured','decorationType','ratings','category','brand','material','ecoFriendlyLevel','code','dimensions','applications','style','imageUrls','stock_quantity','created_at']