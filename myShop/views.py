from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_basket (user):
    if user.is_authenticated:
        return Basket.objects.filter (user = user)
    else:
        return []


def index(request):
    # basket = []
    # if request.user.is_authenticated:
    # basket = Basket.objects.filter (user = request.user)
    basket = get_basket(user = request.user)
    title = 'myShop'
    products = Product.objects.all()[:4]
    links_menu = ['домой', 'продукты', 'контакты',]
    context_page = {
        'title': title,
        'links_menu': links_menu,
        'products': products,
        'basket': basket,
    }
    return render(request, 'myShop/index.html', context=context_page)


def contacts(request):
    # basket = []
    # if request.user.is_authenticated:
    #     basket = Basket.objects.filter (user = request.user)
    basket = get_basket (user = request.user)
    title = 'контакты'
    links_menu = ['домой', 'продукты', 'контакты',]
    context_page = {
        'title': title,
        'links_menu': links_menu,
        'basket': basket,
    }
    return render(request, 'myShop/contacts.html', context=context_page)
