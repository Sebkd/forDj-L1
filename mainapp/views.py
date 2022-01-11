import random

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
from myShop.views import get_basket

def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]

def get_same_products(hot_product):
    same_products = Product.objects.filter(category = hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products

def products(request, pk=None):
    title = 'каталог'
    links_menu = ['домой', 'продукты', 'контакты',]
    cat_products = ProductCategory.objects.all()
    basket = get_basket(user = request.user)
    hot_product = get_hot_product ()
    same_products = get_same_products (hot_product)
    products = Product.objects.all ().order_by ('price')
    # basket = []
    # if request.user.is_authenticated:
    #     basket = Basket.objects.filter (user = request.user)
    #     [
    # {'href': 'products_all', 'name': 'все'},
    # {'href': 'products_home', 'name': 'дом'},
    # {'href': 'products_office', 'name': 'офис'},
    # {'href': 'products_modern', 'name': 'модерн'},
    # {'href': 'products_classic', 'name': 'классика'},
    # ]
   # product = Product.objects.get(id=pk)
    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        context_page = {
            'title': title,
            'links_menu': links_menu,
            'cat_products': cat_products,
            'category': category,
            'products': products,
            'hot_product': hot_product,
            'basket': basket,
            'same_products': same_products,
        }
        return render(request, 'mainapp/products.html', context=context_page)

    # products = Product.objects.all()


    context_page = {
        'title': title,
        'links_menu': links_menu,
        'cat_products': cat_products,
        'hot_product': hot_product,
        'products': products,
        'same_products': same_products,
        'basket': basket,
    }
    return render (request, 'mainapp/products.html', context = context_page)

def product_detail (request, pk):
    title = 'Выбранный продукт'
    links_menu = ['домой', 'продукты', 'контакты', ]
    cat_products = ProductCategory.objects.all ()
    basket = get_basket (user = request.user)
    product = get_object_or_404(Product, pk=pk)
    context_page = {
        'title': title,
        'links_menu': links_menu,
        'cat_products': cat_products,
        'product': product,
        'basket': basket,
    }
    return render (request, 'mainapp/product_detail.html', context = context_page)

# Create your views here.
