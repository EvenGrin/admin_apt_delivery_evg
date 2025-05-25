from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from admin_app.filters import CategoryFilter
from admin_app.forms import CategoryForm
from admin_app.tables import CategoryTable
from admin_app.views import crud_view, confirm_delete_view
from apt_delivery_app.models import Category

@user_passes_test(lambda u: u.is_superuser)
def category_crud_view(request, pk=None):
    return crud_view(request, Category, CategoryForm, pk)

@user_passes_test(lambda u: u.is_superuser)
def category_delete_view(request, pk):
    return confirm_delete_view(request, Category, pk)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class category_list_view(SingleTableMixin, FilterView):
    table_class = CategoryTable
    model = Category
    template_name = "admin_app/list/cabinet_list.html"

    filterset_class = CategoryFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title_plural'] = 'Категории'
        return context
