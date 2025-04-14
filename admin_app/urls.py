from django.urls import path

from admin_app import views

urlpatterns = [
    path('', views.index_view, name='admin_home'),
    path('meal/', views.meal_view, name='admin_meal'),
    path('cab/', views.cab_view, name='admin_cab')
]
