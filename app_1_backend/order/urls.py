from django.urls import path
from . import views
from .views import CheckDeliveryStatus

urlpatterns = [
    path('add', views.AddOrder.as_view(), name='add-order'),
    path('me/', views.UserOrdersBuStatus.as_view(), name='orders-list'),
    path('single/', views.OrderDetails.as_view(), name='order-details'),
    path('check-delivery-status/', CheckDeliveryStatus.as_view(), name='check_delivery_status'),
]
