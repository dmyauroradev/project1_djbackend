from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models, serializers
from django.urls import reverse
from django.db.models import Count
import random
from .models import Product
from django.db import transaction
from .serializers import ProductSerializer
from rest_framework.generics import RetrieveAPIView

class CategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    

class HomeCategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        
        return models.Category.objects.order_by('?')[:6]
    

class ProductList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        
        return models.Product.objects.order_by('?')[:20] 
    
    
class PopularProductsList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        
        return models.Product.objects.filter(ratings__gte=4.0, ratings__lte=5.0).order_by('?')[:20]
    
class ProductListByDecorationType(APIView):
    serializer_class = serializers.ProductSerializer

    def get(self, request):
        query = request.query_params.get('decorationType', None)

        if query:    
            queryset = models.Product.objects.filter(decorationType=query).order_by('?')[:20]
            serializer = serializers.ProductSerializer(queryset, many=True)
            return Response(serializer.data)
        
        else:
            return Response({'message': 'No query provide'}, status=status.HTTP_400_BAD_REQUEST)
        
class SimilarProducts(APIView):

    def get(self, request):
        query = request.query_params.get('category', None)

        if query:
            products = models.Product.objects.filter(category = query).order_by('?')[:6]
            serializer = serializers.ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)
        
class SearchProductByTitle(APIView):
    def get(self, request):
        query = request.query_params.get('q', None)
        print(f"Received search query: {query}")

        if query:
            products = models.Product.objects.filter(title__icontains=query)
            serializer = serializers.ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)
        
class FilterProductByCategory(APIView):
    def get(self, request):
        query = request.query_params.get('category', None)

        if query:
            products = models.Product.objects.filter(category = query)

            serializer = serializers.ProductSerializer(products, many=True)

            return Response(serializer.data)
        else:
            return Response({'message': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)
        
class SellProductView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity_sold = request.data.get('quantity_sold')

        if not product_id or not quantity_sold:
            return Response({'error': 'Product ID and quantity sold are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                product = Product.objects.select_for_update().get(id=product_id)
                if product.stock_quantity >= quantity_sold:
                    product.stock_quantity -= quantity_sold  # Trừ số lượng sản phẩm đã bán
                    product.save()

                    # Lưu thông tin bán hàng
                    sale = models.Sale(product=product, quantity_sold=quantity_sold)
                    sale.save()

                    return Response({'message': 'Product sold successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': f'Not enough stock for product {product.title}. Only {product.stock_quantity} items left.'}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return models.Product.objects.order_by('?')[:20]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # Truyền request để tạo URL đầy đủ
        return context
