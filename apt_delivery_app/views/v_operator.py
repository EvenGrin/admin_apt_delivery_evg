from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from apt_delivery_app.decorators import group_required
from apt_delivery_app.models import Order, Status


@group_required('operator')
@login_required
def operator_orders(request, order='-date_create', filter=0):
    context = {}
    context['order'] = order
    context['filter'] = filter
    context['count'] = Order.objects.all().count()
    context['statuses'] = Status.objects.filter(~Q(id=5))
    orders = Order.objects.all().order_by(order)
    # Все заказы
    if filter:
        orders = Order.objects.filter( status=filter).order_by(order)
    context['orders'] = orders  # Фильтруем заказы
    return render(request, 'operator/order_list.html', context)