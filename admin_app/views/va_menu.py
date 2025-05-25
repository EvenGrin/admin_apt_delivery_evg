from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from admin_app.filters import MenuFilter
from admin_app.forms import MenuForm
from admin_app.tables import MenuTable
from admin_app.views import crud_view
from apt_delivery_app.models import Menu, Meal
from apt_delivery_app.models.m_menu import MenuItem


@method_decorator(login_required, name='dispatch')
class menu_list_view(SingleTableMixin, FilterView):
    table_class = MenuTable
    model = Menu
    filterset_class = MenuFilter
    template_name = "admin_app/list/cabinet_list.html"

    def get_queryset(self):
        return Menu.objects.annotate(items_count=Count('menu_items')).order_by('-date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title_plural'] = 'Меню'
        return context


def menu_crud_view(request, pk=None):
    return crud_view(request, Menu, MenuForm, pk)


# def create_menu(request):
#     if request.method == 'POST':
#         form = MenuForm(request.POST)
#         if form.is_valid():
#             menu = form.save()
#             messages.success(request, 'Меню успешно создано. Теперь добавьте блюда.')
#             return redirect('edit_menu', menu_id=menu.id)
#     else:
#         form = MenuForm(initial={'date': timezone.now().date()})
#
#     return render(request, 'admin_app/edit_form.html', {'form': form})
def create_menu(request):
    return crud_view(request, Menu, MenuForm)


def edit_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    menu_items = menu.menu_items.select_related('meal').all().order_by('meal__category')

    if request.method == 'POST':
        selected_meals = request.POST.getlist('selected_meals')
        for meal_id in selected_meals:
            meal = get_object_or_404(Meal, id=meal_id)
            MenuItem.objects.get_or_create(
                menu=menu,
                meal=meal,
                defaults={'price': meal.price, 'quantity': 1}
            )
        messages.success(request, 'Выбранные блюда добавлены в меню')
        # return redirect('edit_menu', menu_id=menu.id)
        return JsonResponse({
            'success': True,
            'menu_id':menu.id,
            'message': 'Выбранные блюда добавлены в меню'
        })

    # Получаем блюда, которых еще нет в меню
    existing_meal_ids = menu_items.values_list('meal_id', flat=True)
    available_meals = Meal.objects.exclude(id__in=existing_meal_ids).select_related('category')

    # Группируем блюда по категориям
    categories = {}
    for meal in available_meals:
        if meal.category.name not in categories:
            categories[meal.category.name] = []
        categories[meal.category.name].append(meal)

    return render(request, 'admin_app/menu_edit.html', {
        'menu': menu,
        'menu_items': menu_items,
        'categories': categories,
    })


def delete_menu_item(request, menu_id, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id, menu_id=menu_id)
    menu_item.delete()
    messages.success(request, 'Блюдо удалено из меню')
    return redirect('edit_menu', menu_id=menu_id)


class MenuDeleteView(DeleteView):
    model = Menu
    template_name = 'menu/menu_confirm_delete.html'
    success_url = reverse_lazy('menu_list')
    success_message = "Меню успешно удалено"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)