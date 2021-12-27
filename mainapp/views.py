from django.shortcuts import render

from mainapp.models import Product


def products(request, pk):
    title = 'каталог'
    links_menu = ['домой', 'продукты', 'контакты',]
    same_products = [
    {'href': 'products_all', 'name': 'все'},
    {'href': 'products_home', 'name': 'дом'},
    {'href': 'products_office', 'name': 'офис'},
    {'href': 'products_modern', 'name': 'модерн'},
    {'href': 'products_classic', 'name': 'классика'},
    ]
    # product = Product.objects.get(id=pk)
    context_page = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', context=context_page)

# Create your views here.
