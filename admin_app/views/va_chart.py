import json

from django.db.models import OuterRef, ExpressionWrapper, F, Sum, DecimalField, Subquery, Value, Count
from django.db.models.functions import TruncDay, Concat
from django.shortcuts import render

from admin_app.filters import SalesReportFilter
from apt_delivery_app.models import Meal, Order, OrderMeal


# отчет по продажам
def sales_report_view(request):
    filterset = SalesReportFilter(request.GET, queryset=Order.objects.filter(status__code='delivered'))
    orders = filterset.qs

    subquery = OrderMeal.objects.filter(order=OuterRef('pk')).annotate(
        total_price=ExpressionWrapper(F('meal__price') * F('amount'), output_field=DecimalField())
    ).values('order').annotate(total_amount=Sum('total_price')).values('total_amount')

    # Суммарные продажи по дням
    sales_by_day = orders.annotate(
        date=TruncDay('date_create'),
        total_amount=Subquery(subquery),
    ).values('date').annotate(total_sales=Sum('total_amount')).order_by('date')

    # Продажи по категориям
    meal_ids = OrderMeal.objects.filter(order__in=orders).values_list('meal_id', flat=True)

    # 2. Сгруппируем meals по категории и посчитаем total_sales
    sales_by_category = (
        Meal.objects.filter(id__in=meal_ids)
        .values('category__name')
        .annotate(total_sales=Sum('price'))
        .order_by('-total_sales')
    )

    # Продажи по блюдам
    sales_by_dish = (
        Meal.objects.filter(id__in=meal_ids)
        .values('name', 'category__name')
        .annotate(total_sales=Sum('price'))
        .order_by('-total_sales')
    )
    context = {
        'sales_by_day': json.dumps(list(sales_by_day), default=str),
        'sales_by_category': json.dumps(list(sales_by_category)),
        'sales_by_dish': json.dumps(list(sales_by_dish)),
        'title': 'Отчет по продажам',
        'filter': filterset,
    }
    return render(request, 'admin_app/charts/sales_report.html', context)

def user_report_view(request):
    user_type = request.GET.get('user_type', 'all')  # Default to 'all'
    all_clients = Order.objects.values('user__id').distinct().annotate(
        user__username=Concat(
            'user__last_name', Value(' '),
            'user__first_name', Value(' '),
            'user__patronymic'
        ),
        count=Count('user'))
    user_data = {
        'clients': list(all_clients.order_by('-count')),
    }
    # print(user_data)

    context = {
        'user_data': user_data,
        'user_type': user_type,
        'title': 'Отчет по пользователям',
    }
    return render(request, 'admin_app/charts/user_report.html', context)

def courier_report_view(request):
    subquery = OrderMeal.objects.filter(order=OuterRef('pk')).annotate(
        total_price=ExpressionWrapper(F('meal__price') * F('amount'), output_field=DecimalField())
    ).values('order').annotate(total_amount=Sum('total_price')).values('total_amount')

    couriers = (
        Order.objects.filter(deliver__isnull=False)
        .values('deliver')
        .annotate(
            deliver__username=Concat(
                'deliver__last_name', Value(' '),
                'deliver__first_name', Value(' '),
                'deliver__patronymic'
            ),
            count=Count('deliver'),
        )
        .order_by('-count')
    )

    context = {
        'couriers': list(couriers),
        'title': 'Отчет по курьерам',
    }
    return render(request, 'admin_app/charts/courier_report.html', context)
