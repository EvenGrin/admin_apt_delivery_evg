from django.urls import path

from admin_app import views

urlpatterns = [
    path('', views.index_view, name='admin_home'),

    path('meals/', views.meal_list_view.as_view(), name='meal-list'),
    path('meals/add/', views.meal_crud_view, name='meal-add'),  # Добавление блюда
    path('meals/edit/<int:pk>/', views.meal_crud_view, name='meal-edit'),  # Редактирование блюда
    path('meals/delete/<int:pk>/', views.meal_delete_view, name='meal-delete'),  # Удаление блюда

    path('cabinet/', views.cabinet_list_view.as_view(), name='cabinet-list'),
    path('cabinet/add/', views.cabinet_crud_view, name='cabinet-add'),
    path('cabinet/edit/<int:pk>/', views.cabinet_crud_view, name='cabinet-edit'),
    path('cabinet/delete/<int:pk>/', views.cabinet_delete_view, name='cabinet-delete'),

    path('category/', views.category_list_view.as_view(), name='category-list'),
    path('category/add/', views.category_crud_view, name='category-add'),
    path('category/edit/<int:pk>/', views.category_crud_view, name='category-edit'),
    path('category/delete/<int:pk>/', views.category_delete_view, name='category-delete'),

    path('order/', views.order_list_view.as_view(), name='order-list'),
    path('order/<int:pk>', views.order_detail_view, name='order_detail'),
    # path('order/add/', views.order_crud_view, name='order-add'),
    # path('order/edit/<int:pk>/', views.order_crud_view, name='order-edit'),
    # path('order/delete/<int:pk>/', views.order_delete_view, name='order-delete'),

    path ('menu/', views.menu_list_view.as_view(), name='menu-list'),

    path('reports/sales_report/', views.sales_report_view, name='sales_report'),
    path('reports/users_report/', views.user_report_view, name='user_report'),
    path('reports/couriers_report/', views.courier_report_view, name='courier_report'),
]
