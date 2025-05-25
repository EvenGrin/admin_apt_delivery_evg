import django_tables2 as tables
from django.utils.safestring import mark_safe

from apt_delivery_app.models import Cabinet, Category, Meal, Menu, Order


class CabinetTable(tables.Table):
    class Meta:
        model = Cabinet
        fields = ('num', 'name',)

        attrs = {
            'class': 'table table-hover table-bordered table-striped m-0 ',
            'td': {'class': 't-100'},
            'th': {'class': 't-100'},

        }
        row_attrs = {
            "data-id": lambda record: record.id  # Или используйте get_row_attrs()
        }


class MealTable(tables.Table):
    image = tables.Column(attrs={'td': {'class': 'meals_photo'}})

    class Meta:
        model = Meal

        fields = ('image', 'name', 'category', 'price', 'out')

        attrs = {
            'class': 'table table-hover table-bordered table-striped m-0 ',
            'td': {'class': 't-100'},
            'th': {'class': 't-100'},

        }
        row_attrs = {
            "data-id": lambda record: record.id  # Или используйте get_row_attrs()
        }

    def render_image(self, record, value):
        return mark_safe(f"<img src='{record.image.url}' class='rounded img-thumbnail t-50' />")


class CategoryTable(tables.Table):
    class Meta:
        model = Category
        fields = ('name',)

        attrs = {
            'class': 'table table-hover table-bordered table-striped m-0 ',
            'td': {'class': 't-100'},
            'th': {'class': 't-100'},

        }
        row_attrs = {
            "data-id": lambda record: record.id  # Или используйте get_row_attrs()
        }


class MenuTable(tables.Table):

    items_count = tables.Column(verbose_name="Кол-во блюд", empty_values=())
    class Meta:
        model = Menu
        fields = ("date", "items_count",)
        order_by = ("-date",)
        attrs = {
            'class': 'table table-hover table-bordered table-striped m-0 ',
            'td': {'class': 't-100'},
            'th': {'class': 't-100'},

        }
        row_attrs = {
            "data-id": lambda record: record.id  # Или используйте get_row_attrs()
        }

    def render_items_count(self, record):
        return record.menu_items.count()  # Изменили с items на menu_items








class OrderTable(tables.Table):
    def status_attr(record):
        status_id = record.status.id
        css_class = ""
        if status_id == 1:
            css_class = "table-primary"
        elif status_id in [2, 5, 7]:
            css_class = "table-success"
        elif status_id == 3:
            css_class = "table-danger"
        else:
            css_class = "table-secondary"
        return css_class

    status = tables.Column(attrs={'td': {'class': status_attr}})

    class Meta:
        model = Order
        fields = ('user', 'cab', 'order_date', 'deliver', 'status', 'total_amount')

        attrs = {
            'id': 'order-table',
            'class': 'table table-hover table-bordered table-striped m-0 ',
            'thead': {'class': 'sticky-top z-0 shadow-sm'},
            'tbody': {'class': ''},
            "td": {"class": "t-100"},
            "th": {"class": "d-sm-table-cell t-25"}

        }
        order_by = '-date_create'
        row_attrs = {
            "data-order-id": lambda record: record.id  # Или используйте get_row_attrs()
        }
