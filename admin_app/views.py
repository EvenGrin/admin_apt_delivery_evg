from lib2to3.fixes.fix_input import context

from django.shortcuts import render

from apt_delivery_app.models import Meal, Cabinet


# Create your views here.

def index_view(request):
    return render(request, 'admin_app/base.html')

def meal_view(request):
    context = {
        'meals': Meal.objects.all()
    }
    return render(request, 'admin_app/meal.html', context)

def cab_view(request):
    context = {
        'cabs': Cabinet.objects.all()
    }
    return render(request, 'admin_app/cab.html', context)