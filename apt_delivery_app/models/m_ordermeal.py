from django.db import models



class OrderMeal(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name="Заказ")
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE, verbose_name="Блюдо")
    amount = models.IntegerField(verbose_name='Количество товаров')

    class Meta:
        verbose_name = 'Заказ блюд'
        verbose_name_plural = 'Заказы блюд'

    @property
    def total_price(self):
        return self.meal.price * self.amount

    @property
    def total_amount(self):
        return self.meal.price * self.amount

    @property
    def quantity(self):
        return self.amount


    def __str__(self):
        return f'{self.order}'