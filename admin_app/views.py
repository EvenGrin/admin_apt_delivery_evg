import json
from datetime import datetime, timezone
from typing import Any

from django.db.models import OuterRef, ExpressionWrapper, F, Sum, DecimalField, Subquery, Min, Max, Value, Count
from django.db.models.functions import TruncDay, Concat
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django_bootstrap5.renderers import FieldRenderer
from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableMixin

from admin_app.filters import MealFilter, CategoryFilter, CabinetFilter, OrderFilter, SalesReportFilter
from admin_app.forms import MealForm, CategoryForm, CabinetForm
from admin_app.tables import CabinetTable, CategoryTable, MealTable, OrderTable
from apt_delivery_app.models import Meal, Cabinet, Category, Order, OrderMeal, Menu


def generic_list_view(request, model_class, my_filter=None, table=None):
    objects = model_class.objects.all().order_by('-id')
    filtered_objects = objects
    if my_filter:
        filtered_objects = my_filter.qs
    template_name = f'admin_app/list/{model_class.__name__.lower()}_list.html'
    context = {
        f'{model_class.__name__.lower()}s': filtered_objects,
        'filter': my_filter,
        'title_plural': model_class._meta.verbose_name_plural,
    }
    if table:
        RequestConfig(request).configure(table)
        context['table'] = table
    return render(request, template_name, context)


def crud_view(request, model_class, form_class, pk=None):
    instance = None
    if pk:
        instance = get_object_or_404(model_class, pk=pk)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy(f'{model_class.__name__.lower()}-list'))
    else:
        form = form_class(instance=instance)

    context = {
        'title': model_class._meta.verbose_name,
        'url': reverse_lazy(f'{model_class.__name__.lower()}-list'),
        'form': form,
        'object': instance
    }
    return render(request, 'admin_app/edit_form.html', context)


def confirm_delete_view(request, model_class, pk):
    field = get_object_or_404(model_class, pk=pk)
    if request.method == 'POST':
        field.delete()
        return redirect(reverse_lazy(f'{model_class.__name__.lower()}-list'))
    context = {
        'field': field,
        'url': reverse_lazy(f'{model_class.__name__.lower()}-list'),
        'title': model_class._meta.verbose_name
    }
    return render(request, 'admin_app/confirm_delete.html', context)


# Create your views here.

def index_view(request):
    return render(request, 'admin_app/index.html')


#  
# def meal_list_view(request):
#     filter = MealFilter(request.GET, queryset=Meal.objects.all())
#     return generic_list_view(request, Meal, filter)


class meal_list_view(SingleTableMixin, FilterView):
    table_class = MealTable
    model = Meal
    template_name = "admin_app/list/cabinet_list.html"
    filterset_class = MealFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title_plural'] = 'Блюда'
        return context

def meal_crud_view(request, pk=None):
    return crud_view(request, Meal, MealForm, pk)


def meal_delete_view(request, pk):
    return confirm_delete_view(request, Meal, pk)


#
# def category_list_view(request):
#     filter = CategoryFilter(request.GET, Category.objects.all())
#     return generic_list_view(request, Category, filter)


def category_crud_view(request, pk=None):
    return crud_view(request, Category, CategoryForm, pk)


def category_delete_view(request, pk):
    return confirm_delete_view(request, Category, pk)


#
# def cabinet_list_view(request):
#     table = CabinetTable(Cabinet.objects.all())
#     filter = CabinetFilter(request.GET, Cabinet.objects.all())
#     return generic_list_view(request, Cabinet, filter, table)

class category_list_view(SingleTableMixin, FilterView):
    table_class = CategoryTable
    model = Category
    template_name = "admin_app/list/cabinet_list.html"

    filterset_class = CategoryFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title_plural'] = 'Категории'
        return context

class cabinet_list_view(SingleTableMixin, FilterView):
    table_class = CabinetTable
    model = Cabinet
    template_name = "admin_app/list/cabinet_list.html"

    filterset_class = CabinetFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title_plural'] = 'Кабинеты'
        return context


def cabinet_crud_view(request, pk=None):
    return crud_view(request, Cabinet, CabinetForm, pk)


def cabinet_delete_view(request, pk):
    return confirm_delete_view(request, Cabinet, pk)


# 
# def order_list_view(request):
#     filter = OrderFilter(request.GET, Order.objects.all())
#     return generic_list_view(request, Order, filter)


class order_list_view(SingleTableMixin, FilterView):
    table_class = OrderTable
    model = Order
    template_name = "admin_app/list/order_list.html"

    filterset_class = OrderFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title_plural'] = 'Заказы'
        return context

def order_detail_view(request, pk):
    return


#
def menu_view(request):
    return generic_list_view(request, Menu)

# 
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





class CustomFieldRenderer(FieldRenderer):
    def get_server_side_validation_classes(self):
        """Return CSS classes for server-side validation."""
        if self.field_errors:
            return "is-invalid"
        elif self.field.form.is_bound:
            return ""
        return ""
