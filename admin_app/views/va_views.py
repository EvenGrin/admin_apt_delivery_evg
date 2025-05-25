import json
from datetime import datetime, timezone
from typing import Any

from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, ExpressionWrapper, F, Sum, DecimalField, Subquery, Min, Max, Value, Count
from django.db.models.functions import TruncDay, Concat
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django_bootstrap5.renderers import FieldRenderer
from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableMixin

from admin_app.filters import MealFilter, CategoryFilter, CabinetFilter, OrderFilter, SalesReportFilter, MenuFilter
from admin_app.forms import MealForm, CategoryForm, CabinetForm, MenuForm
from admin_app.tables import CabinetTable, CategoryTable, MealTable, OrderTable, MenuTable
from apt_delivery_app.models import Meal, Cabinet, Category, Order, OrderMeal, Menu


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


class CustomFieldRenderer(FieldRenderer):
    def get_server_side_validation_classes(self):
        """Return CSS classes for server-side validation."""
        if self.field_errors:
            return "is-invalid"
        elif self.field.form.is_bound:
            return ""
        return ""
