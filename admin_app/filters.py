import django_filters
from django import forms
from django.forms import DateInput
from django.utils.translation import gettext_lazy as _
from django_filters import widgets


from apt_delivery_app.models import Meal, Category, Cabinet, Order, User, Status

class MyRangeWidget(widgets.RangeWidget):
    def __init__(self, from_attrs=None, to_attrs=None, attrs=None):
        super(MyRangeWidget, self).__init__(attrs)

        if from_attrs:
            self.widgets[0].attrs.update(from_attrs)
        if to_attrs:
            self.widgets[1].attrs.update(to_attrs)



class SalesReportFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="date_create", lookup_expr='gte', widget=DateInput(attrs={'type': 'date'}))
    end_date = django_filters.DateTimeFilter(field_name="date_create", lookup_expr='lte', widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ['start_date', 'end_date']

class MealFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label=_('Название'), lookup_expr='iregex')
    price = django_filters.RangeFilter(widget=widgets.RangeWidget(attrs={'type': 'number'}))
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    price = django_filters.RangeFilter(widget=widgets.RangeWidget({'min':"0", 'type': 'number'}))
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), empty_label="Все категории")



    class Meta:
        model = Meal
        fields = ['name', 'category', 'price']




class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iregex', label=_('Название'))

    class Meta:
        model = Category
        fields = ['name']

class CabinetFilter(django_filters.FilterSet):
    num = django_filters.CharFilter(lookup_expr='iregex', label=_('Номер'))
    name = django_filters.CharFilter(lookup_expr='iregex', label=_('Название'))

    class Meta:
        model = Cabinet
        fields = ['num', 'name']

class OrderFilter(django_filters.FilterSet):
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all())
    date_create = django_filters.DateFromToRangeFilter(widget=widgets.RangeWidget(attrs={'type': 'date'}))
    class Meta:
        model = Order
        fields = ['user', 'status', 'date_create']