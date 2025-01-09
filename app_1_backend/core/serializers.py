from rest_framework import serializers
from . import models
from .models import Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('title', 'id', 'imageUrl')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'
        #extra_fields = ['url']

    

