from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from admin_app.filters import MealFilter
from admin_app.forms import MealForm
from admin_app.tables import MealTable
from admin_app.views import crud_view, confirm_delete_view
from apt_delivery_app.models import Meal


@method_decorator(login_required, name='dispatch')
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
