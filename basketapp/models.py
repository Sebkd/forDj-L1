from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Product


# не нужно использовать при использовании сигналов @receiver в orderapp/view
# class BasketQuerySet(models.QuerySet):
#
#     def delete(self, *args, **kwargs):
#         for obj in self:
#             obj.product.quantity += obj.quantity
#             obj.product.save()
#         super(self.__class__, self).delete(*args, **kwargs)


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager() # обработка моделей ведется через отдельный класс, но так как там
    # только один метод переопределен delete, то и касается он только одного метода
    # не нужно использовать при использовании сигналов @receiver в orderapp/view

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # можно указать и 'authapp.ShopUser'
        on_delete=models.CASCADE,
        related_name='basket',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0
    )
    add_datetime = models.DateTimeField(
        verbose_name='время создания',
        auto_now_add=True
    )

    @cached_property
    def get_items_cashed(self):
        return self.user.basket.select_related()

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        # _items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cashed #кэширование, заменяем верхний метод
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        # _items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cashed #кэширование
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost



    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    def save(self, *args, **kwargs):  # не нужно использовать одновременно с сигналами, @receiver
        if self.pk:  # если это объект, а если есть рк то точно объект
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
            # склад = склад - разница в корзине из (кол-во сейчас - кол-во прежде)
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)

    # не совсем правильное добавление на склад с удалением из корзины
    # def delete(self):# добавление к удалению
    #     self.product.quantity += self.quantity # при удалении из корзины, увеличивается кол-во на складе продукта
    #     self.product.save() # сохранение продукта на складе
    #     super(self.__class__, self).delete() # передача родительскому классу, чтобы он отработал

# Create your models here.
