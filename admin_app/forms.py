from django import forms

from apt_delivery_app.models import Meal, Category, Cabinet


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
