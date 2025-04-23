from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django_bootstrap5.renderers import FieldRenderer

from admin_app.filters import MealFilter, CategoryFilter, CabinetFilter, OrderFilter
from admin_app.forms import MealForm, CategoryForm, CabinetForm
from apt_delivery_app.models import Meal, Cabinet, Category, Order


def generic_list_view(request, model_class, my_filter):
    objects = model_class.objects.all().order_by('-id')

    filtered_objects = my_filter.qs
    template_name = f'admin_app/{model_class.__name__.lower()}_list.html'
    context = {
        f'{model_class.__name__.lower()}s': filtered_objects,
        'filter': my_filter,
    }
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
    return render(request, 'admin_app/base.html')


def meal_list_view(request):
    filter = MealFilter(request.GET, queryset=Meal.objects.all())
    return generic_list_view(request, Meal, filter)


def meal_crud_view(request, pk=None):
    return crud_view(request, Meal, MealForm, pk)


def meal_delete_view(request, pk):
    return confirm_delete_view(request, Meal, pk)


def category_list_view(request):
    filter = CategoryFilter(request.GET, Category.objects.all())
    return generic_list_view(request, Category, filter)


def category_crud_view(request, pk=None):
    return crud_view(request, Category, CategoryForm, pk)


def category_delete_view(request, pk):
    return confirm_delete_view(request, Category, pk)


def cabinet_list_view(request):
    filter = CabinetFilter(request.GET, Cabinet.objects.all())
    return generic_list_view(request, Cabinet, filter)


def cabinet_crud_view(request, pk=None):
    return crud_view(request, Cabinet, CabinetForm, pk)


def cabinet_delete_view(request, pk):
    return confirm_delete_view(request, Cabinet, pk)


def order_list_view(request):
    filter = OrderFilter(request.GET, Order.objects.all())
    return generic_list_view(request, Order, filter)


class CustomFieldRenderer(FieldRenderer):
    def get_server_side_validation_classes(self):
        """Return CSS classes for server-side validation."""
        if self.field_errors:
            return "is-invalid"
        elif self.field.form.is_bound:
            return ""
        return ""
#     def get_server_side_validation_classes(self):
#         if self.field_errors:
#             return self.error_css_class
#         elif self.field.form.is_bound:
#             return self.success_css_class


