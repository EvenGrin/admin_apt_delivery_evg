
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from io import BytesIO
import pyqrcode

import os
import django
import sys
# Добавьте это перед импортом моделей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from apt_delivery_app.forms import RegisterForm
from apt_delivery_app.models import Order, User, Status


class RegistrationTest(TestCase):
    def test_registration_validation(self):
        url = reverse('registration')
        invalid_data = {
            'username': 'логin',
            'first_name': 'Ваня1',
            'last_name': 'Iванов',
            'email': 'log@log',
            'password1': '123',
            'password2': '321'
        }
        response = self.client.post(url, invalid_data)
        form = RegisterForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertFormError(form, 'username', 'Разрешенные символы (латиница, цифры и тире).')
        self.assertFormError(form, 'email', 'Введите правильный адрес электронной почты.')
        self.assertFormError(form, 'password2', 'Введенные пароли не совпадают.')

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_email_validation(self):
        with self.assertRaises(ValidationError):
            user = User(
                username='baduser',
                email='invalid-email',
                password='testpass123'
            )
            user.full_clean()  # Вызывает валидацию модели





class OrderCancellationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.order = Order.objects.create(user=self.user, status=Status.objects.get(code='new'))

    def test_order_cancellation(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('cancel_order', args=[self.order.id])

        # Проверяем, что кнопка отмены доступна
        detail_response = self.client.get(reverse('order'))
        print(detail_response)
        self.assertContains(detail_response, f'data-id="{self.order.id}"')

        # Проверяем отмену
        response = self.client.get(url)
        self.order.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.order.status.code, 'canceled')


class QRCodeGenerationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.order = Order.objects.create(
            user_id=1,
            qr_code="order_1_abc123"
        )

    def test_generate_qr_code(self):
        """
        TC_API_1: Проверка генерации QR-кода
        """
        response = self.client.get(
            reverse('generate_qr', args=[self.order.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('image/svg+xml', response['Content-Type'])

        # Проверка содержимого QR-кода
        qr = pyqrcode.create(f"order_{self.order.id}_abc123")
        buffer = BytesIO()
        qr.svg(buffer, scale=1)
        self.assertGreater(len(response.content), len(buffer.getvalue()) // 2)


class PaymentConfirmationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.order = Order.objects.create(
            user_id=1,
            qr_code="order_1_valid"
        )

    def test_valid_qr_confirmation(self):
        """
        TC_API_2: Подтверждение оплаты по валидному QR-коду
        """
        response = self.client.get(
            reverse('confirm_payment'),
            {'qr_code': self.order.qr_code},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'status': 'success',
            'message': 'Оплата подтверждена'
        })
        self.order.refresh_from_db()
        self.assertTrue(self.order.is_paid)

    def test_invalid_qr_confirmation(self):
        """
        TC_API_3: Обработка неверного QR-кода
        """
        response = self.client.get(
            reverse('confirm_payment'),
            {'qr_code': 'invalid_code'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'status': 'error',
            'message': 'Заказ не найден'
        })