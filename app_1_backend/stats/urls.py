from django.urls import path
from . import views

urlpatterns = [
    path('api/stats/revenue/', views.RevenueStatsView.as_view(), name='revenue-stats'),
    path('api/stats/users/', views.UserGrowthStatsView.as_view(), name='user-stats'),
    path('api/stats/orders/', views.OrderStatsView.as_view(), name='order-stats'),
    path('api/stats/top-selling/', views.BestSellingProductsView.as_view(), name='top-selling-stats'),
    path('statistics/', views.statistics_page, name='statistics-page'),
    path('api/stats/daily-product-stock/', views.DailyProductStockStatsView.as_view(), name='daily-product-stock-stats'),
    path('api/stats/monthly-product-stock/', views.MonthlyProductStockStatsView.as_view(), name='monthly-product-stock-stats'),
    path("api/stats/top-users-by-orders/", views.TopUsersByOrdersView.as_view(), name="top-users-by-orders"),
]