from django import forms

from apt_delivery_app.models import Meal, Category, Cabinet, Menu
from apt_delivery_app.models.m_menu import MenuItem


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields=('image', 'name', 'category', 'price', 'out', 'quantity',)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class CabinetForm(forms.ModelForm):
    class Meta:
        model = Cabinet
        fields = ['num', 'name']

class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ['date']

class MenuItemForm(forms.ModelForm):

    class Meta:
        model = MenuItem
        fields = ['meal','price','quantity']