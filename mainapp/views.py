from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def products(request, pk=None):
    title = 'каталог'
    links_menu = ['домой', 'продукты', 'контакты',]
    cat_products = ProductCategory.objects.all()
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter (user = request.user)
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
            'basket': basket,
        }
        return render(request, 'mainapp/products.html', context=context_page)

    products = Product.objects.all()
    context_page = {
        'title': title,
        'links_menu': links_menu,
        'cat_products': cat_products,
        'products': products,
        'basket': basket,
    }
    return render (request, 'mainapp/products.html', context = context_page)

# Create your views here.
