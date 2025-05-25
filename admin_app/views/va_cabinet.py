from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from admin_app.filters import CabinetFilter
from admin_app.forms import CabinetForm
from admin_app.tables import CabinetTable
from admin_app.views import crud_view, confirm_delete_view
from apt_delivery_app.models import Cabinet


@method_decorator(login_required, name='dispatch')
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
