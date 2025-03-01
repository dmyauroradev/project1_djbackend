from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from . import models, serializers
from notification.models import Notification
from core.models import Product
from stats.models import Sale
from extras.models import Address
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from order.models import Order
from django.core.cache import cache

def json_response(data, status=status.HTTP_200_OK):
    return Response(data, status=status, content_type="application/json; charset=utf-8")

class AddOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        print("Received data in Django:", data) 
        print("Auth token:", request.auth)
        print("User:", request.user)

        valid_statuses = ['pending', 'đang giao', 'đã giao'] 

        if "delivery_status" not in data or data["delivery_status"] not in valid_statuses:
            return Response({"message": "Invalid delivery status"}, status=status.HTTP_400_BAD_REQUEST)

        
        try:
            with transaction.atomic():
                validated_products = []
                address = get_object_or_404(Address, id=int(data['address']))

                for product_data in data['order_products']:
                    product = get_object_or_404(Product, id=product_data ['product'])

                    if product.stock_quantity < product_data["quantity"]:
                        return Response({
                            "message": f"Không đủ hàng cho sản phẩm {product.title}. Chỉ còn {product.stock_quantity} sản phẩm trong kho."
                        }, status=status.HTTP_400_BAD_REQUEST)

                    # Deduct stock quantity
                    product.stock_quantity -= product_data["quantity"]
                    product.save()

                    validated_products.append(
                        {
                            "product_id": product.id,
                            "imageUrl": product.imageUrls[0],
                            "title": product.title,
                            "price": int(product.price),
                            "quantity": product_data["quantity"],
                            "dimensions": product_data["dimensions"],
                            "code": product_data["code"]
                        }
                    )

                    # Tạo bản ghi Sale
                    Sale.objects.create(
                        product=product,
                        quantity_sold=product_data["quantity"]
                    )

                    #address = get_object_or_404(Address, id = int(data['address']))

                order = models.Order.objects.create(
                    user = request.user,
                    customer_id = data["customer_id"],
                    address = address,
                    order_products = validated_products,
                    rated = [0],
                    total_quantity = data['total_quantity'],
                    subtotal = int(data['subtotal']),
                    total = int(data['total']),
                    delivery_status = data["delivery_status"],
                    payment_status = data["payment_status"]
                )
                #print(Order.objects.values_list('delivery_status', flat=True).distinct())



                    # create notification
                title = "Đặt Hàng Thành Công"
                message = "Thanh toán của bạn đã được hoàn tất và đơn hàng của bạn hiện đang được xử lý"

                Notification.objects.create(
                    orderId = order,
                    title = title,
                    message = message,
                    userId = request.user
                )


                return Response({"id": order.id}, status=status.HTTP_201_CREATED)
                
        except Product.DoesNotExist:
                return Response({"message": "one or more products not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Address.DoesNotExist:
            return Response({"message": "one address does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        except KeyError as e:
            return Response({"message": f"Missing key: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class UserOrdersBuStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order_status = request.query_params.get('status')
        user = request.user
        
        valid_statuses = ['pending', 'shipping', 'delivered'] 

        if order_status and order_status not in valid_statuses:
            return Response({"message": "Invalid delivery status"}, status=status.HTTP_400_BAD_REQUEST)

        if order_status:
            orders = models.Order.objects.filter(user=user, delivery_status=order_status).order_by('-created_at')
        else:
            orders = models.Order.objects.filter(user=user).order_by('-created_at')    

        serializer = serializers.OrdersSerializer(orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order_id = request.query_params.get('id')

        order = get_object_or_404(models.Order, id=order_id)

        serializer = serializers.OrdersSerializer(order)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CheckDeliveryStatus(APIView):
    def get(self, request):
        statuses = Order.objects.values_list('delivery_status', flat=True).distinct()
        return Response({"delivery_statuses": statuses})