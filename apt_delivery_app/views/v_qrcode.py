from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from apt_delivery_app.models import Order
import pyqrcode
from io import BytesIO


def generate_qr(request, order_id):
    order = Order.objects.get(id=order_id)
    # URL для подтверждения оплаты
    confirmation_url = request.build_absolute_uri(
        reverse('confirm_payment')
    ) + f"?qr_code={order.qr_code}"

    # Генерируем QR-код
    qr = pyqrcode.create(confirmation_url)

    # Создаем поток для ответа
    buffer = BytesIO()
    qr.svg(buffer, scale=5)

    response = HttpResponse(buffer.getvalue(), content_type="image/svg+xml")
    return response

@csrf_exempt  # Для упрощения, можно заменить на правильную CSRF защиту для API
def confirm_payment(request):
    if request.method == 'POST':
        qr_code = request.POST.get('qr_code')
        try:
            order = Order.objects.get(qr_code=qr_code)
            if not order.is_paid:
                order.is_paid = True
                order.save()
                return JsonResponse({'status': 'success', 'message': 'Оплата подтверждена'})
            return JsonResponse({'status': 'info', 'message': 'Заказ уже оплачен'})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Заказ не найден'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'}, status=400)