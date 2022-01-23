from django.db import transaction
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from basketapp.models import Basket
from orderapp.forms import OrderItemForm
from orderapp.models import Order, OrderItem


class OrderList(ListView):
    model = Order
    links_menu = ['домой', 'продукты', 'контакты', ]
    extra_context = {'links_menu': links_menu}

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)  # кто запросил тот и видит


class OrderCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:order_list')

    links_menu = ['домой', 'продукты', 'контакты', ]
    extra_context = {'links_menu': links_menu}

    def get_context_data(self, **kwargs):  # что передать на страницу, переопределить
        context = super(OrderCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        # формирование таблички из двух моделей по форме, 1 табличка

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)  # проверяем корзину
            if len(basket_items):  # если корзина не пустая то заполняем заказы из нее,
                # количество табличек равно количеству товаром из корзинки
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm,
                                                     extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                    # basket_items[num].delete()  # но это не оптимально, так как он каждую позицию удаляет, а не очередью
                basket_items.delete()
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            # добавляем юзера так как удалили его в форме, а он является foreignkey в модели
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:order_list')

    links_menu = ['домой', 'продукты', 'контакты', ]
    extra_context = {'links_menu': links_menu}

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        context['orderitems'] = formset

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orderapp:order_list')

    links_menu = ['домой', 'продукты', 'контакты', ]
    extra_context = {'links_menu': links_menu}


class OrderRead(DetailView):
    model = Order
    links_menu = ['домой', 'продукты', 'контакты', ]
    extra_context = {
        'links_menu': links_menu,
        'title': 'заказ/просмотр',
    }


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('orderapp:order_list'))

# методы сигналов для удаления из склада и добавления в него
@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields is 'quantity' or 'product':
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
# Create your views here.
