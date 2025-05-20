from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from apt_delivery_app.decorators import group_required
from apt_delivery_app.models import Order, Status

@group_required('operator')
@login_required
def confirm_operator_list(request, order='-date_create', filter=0):
    context = {}
    context['title'] = 'Проверка заказов'
    context['order'] = order
    context['filter'] = filter
    context['statuses'] = Status.objects.filter(~Q(id=5))
    context['orders'] = Order.objects.filter(status__code='new').order_by(order)  # Фильтруем заказы
    return render(request, 'operator/order_list.html', context)

@group_required('operator')
@login_required
def operator_orders(request, order='-date_create', filter=0):
    context = {}
    context['title'] = 'Отправка заказов'
    context['order'] = order
    context['filter'] = filter
    context['count'] = Order.objects.filter(status__code='confirmed').count()
    context['statuses'] = Status.objects.filter(~Q(id=5))
    orders = Order.objects.filter(status__code='confirmed').order_by(order)
    # Все заказы
    if filter:
        orders = Order.objects.filter( status=filter).order_by(order)
    context['orders'] = orders  # Фильтруем заказы
    return render(request, 'operator/order_list.html', context)

@login_required
@group_required('operator')
@require_POST
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.confirm():
        return JsonResponse({
            'status': 'success',
            'message': 'Заказ успешно подтвержден!',
            'new_status': order.status.name,
            'status_value': order.status.id
        })
    return JsonResponse({
        'status': 'error',
        'message': 'Невозможно подтвердить заказ в текущем статусе.'
    })

@login_required
@group_required('operator')
@require_POST
def cancel_operator_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.cancel():
        return JsonResponse({
            'status': 'success',
            'message': 'Заказ успешно отменен!',
            'new_status': order.status.name,
            'status_value': order.status.id
        })
    return JsonResponse({
        'status': 'error',
        'message': 'Невозможно отменить заказ в текущем статусе.'
    })