from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from apt_delivery_app import views

urlpatterns = [
    path('favicon.ico', lambda _: redirect('static/images/logo.png', permanent=True)),
    #
    path('admin/', admin.site.urls),
    path('admin_app/', include('admin_app.urls')),
    #
    path('', views.meal_list, name="home"),
    path('menu', views.menu, name='menu'),
    #
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/registration', views.register_view, name='registration'),
    path('logout/', views.logout_view, name='logout'),
    #
    path('cart/', views.cart, name="cart"),
    path('cart/make_order', views.make_order, name="make_order"),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('sub-from-cart/', views.sub_from_cart, name='sub_from_cart'),
    path('cart_empty/', views.cart_empty, name='cart_empty'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    #
    path('deliver/deliver_orders/', views.deliver_orders, name="deliver_orders"),
    path('deliver/deliver_orders/<int:pk>', views.deliver_order_modal, name='deliver_order_modal'),
    path('deliver/deliver_orders/<str:order>/<int:filter>', views.deliver_orders, name="deliver_orders"),
    path('deliver/order_list/', views.take_order_list, name="deliver"),
    path('deliver/order_list/<str:order>/<int:filter>', views.take_order_list, name="deliver"),
    path('deliver/take_order/', views.take_order, name="take_order"),
    path('deliver/update_status/', views.update_status, name="update_status"),
    #
    path('api/confirm-payment/', views.confirm_payment, name='confirm_payment'),
    path('order/<int:order_id>/qr/', views.generate_qr, name='generate_qr'),
    #
    path('operator/orders/', views.operator_orders, name="operator_orders"),
    path('operator/order/<int:order_id>/confirm/', views.confirm_order, name='confirm_order'),
    path('operator/order/<int:order_id>/change_status/', views.change_status, name='change_status_order'),
    path('operator/order/<int:order_id>/cancel/', views.cancel_operator_order, name='cancel_order'),
    path('operator/confirm_order_list/', views.confirm_operator_list, name="operator"),
    path('operator/confirm_order_list/<str:order>/<int:filter>', views.confirm_operator_list, name="operator"),
    path('operator/orders/<str:order>/<int:filter>', views.operator_orders, name="operator_orders"),
    #
    path('order/', views.order, name="order"),
    path('orders/cancel/<int:id>', views.cancel_order, name='cancel_order'),
    path('order/<str:order_by>/<int:filter>', views.order, name="order"),
    # path('order/<int:pk>/edit', views.order_update, name='order_update'),
    path('order/<int:pk>/', views.order_modal, name='order_modal'),
    path('order/edit', views.order_update, name='order_update'),
    path('add-to-order/', views.add_to_order, name='add_to_order'),
    path('sub-from-order/', views.sub_from_order, name='sub_from_order'),
    #

]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
