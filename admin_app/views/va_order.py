from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from admin_app.filters import OrderFilter
from admin_app.tables import OrderTable
from apt_delivery_app.models import Order


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class order_list_view(SingleTableMixin, FilterView):
    table_class = OrderTable
    model = Order
    template_name = "admin_app/list/order_list.html"

    filterset_class = OrderFilter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title_plural'] = 'Заказы'
        return context

@user_passes_test(lambda u: u.is_superuser)
def order_detail_view(request, pk):
    return
