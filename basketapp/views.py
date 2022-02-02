from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product
from myShop.views import get_basket

from django.contrib.auth.decorators import login_required


@login_required
def basket(request):
    # basket = get_basket (user = request.user)
    # basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
    # 18 запросов, 4-6 мс
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category').select_related()
    # 13 запросов, 3-4 мс
    title = 'Корзина'
    links_menu = ['домой', 'продукты', 'контакты', ]
    context_page = {
        'title': title,
        'links_menu': links_menu,
        'basket_items': basket_items,
        # 'basket': basket
    }
    return render(request, 'basketapp/basket.html', context=context_page)


@login_required
def basket_add(request, pk):
    # if 'login' in request.META.get('HTTP_REFERER'):
    #     return HttpResponseRedirect(reverse('products:product_detail', args=[pk]))
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).select_related().first()
    # корзинок может
    # быть много, берем первую из них (последнюю созданную)

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product_detail', args=[pk]))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if (request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'):
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = get_basket(user=request.user).order_by('product__category').select_related()

        context = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', context)

        return JsonResponse({'result': result})

# Create your views here.
