from django.urls import path

from admin_app import views

urlpatterns = [
    path('', views.index_view, name='home_admin')
]