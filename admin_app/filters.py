import django_filters
from django.utils.translation import gettext_lazy as _
from django_filters.widgets import RangeWidget

from apt_delivery_app.models import Meal, Category, Cabinet, Order, User, Status


class MealFilter(django_filters.FilterSet):
    # Здесь определяем поля для фильтрации и настраиваем фильтры
    name = django_filters.CharFilter(label=_('Название'), lookup_expr='iregex')
    price = django_filters.RangeFilter()
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Meal
        fields = ['name', 'price', 'category']

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
    date_create = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ['user', 'status', 'date_create']