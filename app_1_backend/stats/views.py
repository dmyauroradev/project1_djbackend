from django.shortcuts import render 
from django.db.models import Sum, Count, F
from django.utils.timezone import now, make_aware, is_naive, get_current_timezone 
from datetime import timedelta, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RevenueStatsSerializer, UserGrowthStatsSerializer, OrderStatsSerializer, BestSellingProductsSerializer
from order.models import Order
from django.contrib.auth.models import User
from stats.models import Sale, Product
from django.db.models.functions import TruncDay, TruncMonth
from collections import defaultdict

def make_aware_if_naive(date):
    if isinstance(date, datetime) and is_naive(date):
        return make_aware(date, get_current_timezone())
    return date

# Revenue over time
class RevenueStatsView(APIView):
    def get(self, request):
        months = int(request.query_params.get("months", 12))
        end_date = now().date()
        start_date = end_date - timedelta(days=30*months)

        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

        start_date = make_aware_if_naive(start_date)
        end_date = make_aware_if_naive(end_date)
        
        revenue_stats = (
            Sale.objects.filter(sale_date__range=[start_date, end_date])
            .annotate(month=F('sale_date__month'), year=F('sale_date__year'))
            .values('year', 'month')
            .annotate(revenue=Sum(F('quantity_sold') * F('product__price')))
            .order_by('year', 'month')
        )
        
    
        labels = [f"{item['month']}/{item['year']}" for item in revenue_stats]
        data = [item['revenue'] for item in revenue_stats]
        return Response({"labels": labels, "data": data})


# User growth over time
class UserGrowthStatsView(APIView):
    def get(self, request):
        months = int(request.query_params.get("months", 12))
        end_date = now().date()
        start_date = end_date - timedelta(days=30*months)

        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

        start_date = make_aware_if_naive(start_date)
        end_date = make_aware_if_naive(end_date)

        
        user_growth_stats = (
            User.objects.filter(date_joined__range=[start_date, end_date])
            .annotate(month=F('date_joined__month'), year=F('date_joined__year'))
            .values('year', 'month')
            .annotate(user_count=Count('id'))
            .order_by('year', 'month')
        )
        
        labels = [f"{item['month']}/{item['year']}" for item in user_growth_stats]
        data = [item['user_count'] for item in user_growth_stats]
        
        return Response({"labels": labels, "data": data})

# Orders over time
class OrderStatsView(APIView):
    def get(self, request):
        months = int(request.query_params.get("months", 12))
        end_date = now().date()
        start_date = end_date - timedelta(days=months * 30)

        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

        start_date = make_aware_if_naive(start_date)
        end_date = make_aware_if_naive(end_date)

        
        order_stats = (
            Order.objects.filter(created_at__range=[start_date, end_date])
            .annotate(month=F('created_at__month'), year=F('created_at__year'))
            .values('year', 'month')
            .annotate(order_count=Count('id'))
            .order_by('year', 'month')
        )
        
        labels = [f"{item['month']}/{item['year']}" for item in order_stats]
        data = [item['order_count'] for item in order_stats]
        
        return Response({"labels": labels, "data": data})


# Best-selling products
class BestSellingProductsView(APIView):
    def get(self, request):
        months = int(request.query_params.get("months", 12))
        end_date = now().date()
        start_date = end_date - timedelta(days=months * 30)

        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

        start_date = make_aware_if_naive(start_date)
        end_date = make_aware_if_naive(end_date)

        best_selling_products = (
            Sale.objects.filter(sale_date__range=[start_date, end_date])
            .annotate(month=F('sale_date__month'), year=F('sale_date__year'))
            .values('year', 'month', 'product__title')
            .annotate(total_quantity_sold=Sum('quantity_sold'))
            .order_by('year', 'month','-total_quantity_sold')
        )
        
        # Nhóm dữ liệu theo ngày và sản phẩm
        grouped_data = {}
        for item in best_selling_products:
            key = f"{item['month']}/{item['year']}"
            product = item['product__title']
            quantity = item['total_quantity_sold']
            if key not in grouped_data:
                grouped_data[key] = {}
            grouped_data[key][product] = quantity

        # Lấy danh sách ngày (labels)
        labels = sorted(grouped_data.keys())

        # Lấy danh sách sản phẩm (đảm bảo tất cả sản phẩm đều có mặt trong datasets)
        all_products = set(
            item['product__title'] for item in best_selling_products
        )

        # Tạo dữ liệu đầy đủ, đảm bảo giá trị mặc định là 0
        datasets = {product: [0] * len(labels) for product in all_products}

        for i, date in enumerate(labels):
            for product in all_products:
                datasets[product][i] = grouped_data.get(date, {}).get(product, 0)

        # Chuẩn bị dữ liệu trả về
        return Response({
            "labels": labels,
            "datasets": [
                {"label": product, "data": datasets[product]} for product in datasets
            ]
        })
    
class TopUsersByOrdersView(APIView):
    def get(self, request):
        months = int(request.query_params.get("months", 12))  # Mặc định 12 tháng
        end_date = now().date()
        start_date = end_date - timedelta(days=months * 30)

        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

        start_date = make_aware_if_naive(start_date)
        end_date = make_aware_if_naive(end_date)


        # Lấy số lượng đơn hàng của từng user trong khoảng thời gian
        top_users_stats = (
            Order.objects.filter(created_at__range=[start_date, end_date])
            .annotate(month=F('created_at__month'), year=F('created_at__year'), username=F('user__username')) 
            .values("year", "month", "username")  
            .annotate(total_orders=Count("id"))  # Tổng số đơn hàng
            .order_by("year", "month", "-total_orders")  # Sắp xếp theo số đơn giảm dần
        )

        # Nhóm dữ liệu theo tháng
        grouped_data = defaultdict(list)
        for item in top_users_stats:
            month = f"{item['month']:02d}/{item['year']}"
            grouped_data[month].append({
                "username": item["username"],
                "orders": item["total_orders"]
            })
            # Lấy danh sách các tháng có dữ liệu
        all_months = sorted(grouped_data.keys())  # Chỉ các tháng có dữ liệu
        
        # Tổng hợp dữ liệu cho từng người dùng
        all_users = {item['username'] for sublist in grouped_data.values() for item in sublist}
        user_data = {user: [0] * len(all_months) for user in all_users}

        for i, month in enumerate(all_months):
            for user in grouped_data.get(month, []):
                user_data[user['username']][i] = user['orders']

        # Chuyển đổi sang định dạng datasets
        datasets = [{"label": user, "data": user_data[user]} for user in user_data]

        return Response({"labels": all_months, "datasets": datasets})
    
def statistics_page(request):
    return render(request, 'stats/statistics.html')

# Thống kê tồn kho theo từng sản phẩm, theo ngày
class DailyProductStockStatsView(APIView):
    def get(self, request):
        days = int(request.query_params.get("days", 30))
        end_date = now()
        start_date = end_date - timedelta(days=days)

        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

        start_date = make_aware_if_naive(start_date)
        end_date = make_aware_if_naive(end_date)


        stock_stats = (
            Product.objects.all()
            .annotate(date=TruncDay('updated_at'))  # Nhóm theo ngày
            .filter(date__range=[start_date, end_date])
            .values('date', 'title')  # Lấy theo ngày và tên sản phẩm
            .annotate(total_stock=Sum('stock_quantity'))  # Tổng tồn kho
            .order_by('date', 'title')  # Sắp xếp theo ngày và tên sản phẩm
        )

        data = [
            {
                "date": item["date"].strftime("%Y-%m-%d"),
                "product": item["title"],
                "total_stock": item["total_stock"]
            }
            for item in stock_stats
        ]
        return Response(data)


# Thống kê tồn kho theo từng sản phẩm, theo tháng
class MonthlyProductStockStatsView(APIView):
    def get(self, request):
        months = int(request.query_params.get("months", 12))  # Mặc định 12 tháng
        end_date = now().date() #.replace(day=1)  # Ngày đầu tiên của tháng hiện tại
        start_date = end_date - timedelta(days=months * 30)

        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

        start_date = make_aware_if_naive(start_date)
        end_date = make_aware_if_naive(end_date)


        stock_stats = (
            Product.objects.all()
            .annotate(month=TruncMonth('updated_at'))  # Nhóm theo tháng
            .filter(month__range=[start_date, end_date])
            .values('month', 'title')  # Lấy theo tháng và tên sản phẩm
            .annotate(total_stock=Sum('stock_quantity'))  # Tổng tồn kho
            .order_by('month', 'title')  # Sắp xếp theo tháng và tên sản phẩm

        )

        if not stock_stats.exists():
            return Response({"message": "No data available for the given range."}, status=200)

        data = [
            {
                "month": item["month"].strftime("%Y-%m") if item["month"] else None,
                "product": item["title"],
                "total_stock": item["total_stock"]
            }
            for item in stock_stats
        ]
        return Response(data)
    
