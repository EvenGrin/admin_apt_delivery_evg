import django
from django.db import models

from apt_delivery_app.models import Meal


class MenuItem(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='menu_items')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество", blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name="Стоимость", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.quantity is None:
            self.quantity = self.meal.quantity
        if not self.price:
            self.price = self.meal.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.menu}: {self.meal}"

    class Meta:
        unique_together = ('menu', 'meal',)
        verbose_name = 'Элемент меню'
        verbose_name_plural = 'Элементы меню'


class Menu(models.Model):
    date = models.DateField(
        default=django.utils.timezone.now,
        verbose_name='Дата',
        unique=True,
    )
    meal = models.ManyToManyField(
        Meal,
        through=MenuItem,
        verbose_name='Блюдо',
    )

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
