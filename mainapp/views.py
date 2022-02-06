import random

from django.shortcuts import render, get_object_or_404

from mainapp.models import Product, ProductCategory

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import never_cache # если не хотим кэшировать какую то функцию


def get_links_menu():
    """
    функция для кэша по memocached
    """
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    """
    функция для кэша по memocached
    """
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        _category_cached = cache.get(key)
        if _category_cached is None:
            _category_cached = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, _category_cached)
        return _category_cached
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    """
    функция для кэша по memocached
    """
    if settings.LOW_CACHE:
        key = 'products'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(is_active=True)
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(is_active=True)


def get_product(pk):
    """
    функция для кэша по memocached
    """
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        _product = cache.get(key)
        if _product is None:
            _product = get_object_or_404(Product, pk=pk)
            cache.set(key, _product)
        return _product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orderd_by_price():
    """
    функция для кэша по memocached
    """
    if settings.LOW_CACHE:
        key = 'products_orderd_by_price'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orderd_by_price(pk):
    """
    функция для кэша по memocached
    """
    if settings.LOW_CACHE:
        key = f'products_in_category_orderd_by_price_{pk}'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True)\
                .order_by('price')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True)\
                .order_by('price')


def get_hot_product():
    # products = Product.objects.all() кэшируем
    products = get_products()
    return random.sample(list(products), 1)[0]



def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products

@cache_page(3600)
def products(request, pk=None, page=1):
    title = 'каталог'
    links_menu = ['домой', 'продукты', 'контакты', ]
    # cat_products = ProductCategory.objects.all() # to cached
    cat_products = get_links_menu()
    # basket = get_basket(user = request.user)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    # products = Product.objects.all().order_by('price') # to cached
    products = get_products_orderd_by_price()
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
            # products = Product.objects.all().order_by('price') # to cached
            products = get_products_orderd_by_price()
            category = {
                'pk': 0,
                'name': 'все'}
        else:
            # category = get_object_or_404(ProductCategory, pk=pk) # to cached
            category = get_category(pk)
            # products = Product.objects.filter(category__pk=pk).order_by('price') # to cached
            products = get_products_in_category_orderd_by_price(pk)

        paginator = Paginator(products, 1)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context_page = {
            'title': title,
            'links_menu': links_menu,
            'cat_products': cat_products,
            'category': category,
            'products': products_paginator,
            'hot_product': hot_product,
            # 'basket': basket,
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
        # 'basket': basket,
    }
    return render(request, 'mainapp/products.html', context=context_page)


def product_detail(request, pk):
    title = 'Выбранный продукт'
    links_menu = ['домой', 'продукты', 'контакты', ]
    # cat_products = ProductCategory.objects.all() # to cached
    cat_products = get_links_menu()
    # basket = get_basket (user = request.user)
    # product = get_object_or_404(Product, pk=pk) # to cached
    product = get_product(pk)
    context_page = {
        'title': title,
        'links_menu': links_menu,
        'cat_products': cat_products,
        'product': product,
        # 'basket': basket,
    }
    return render(request, 'mainapp/product_detail.html', context=context_page)

# Create your views here.
