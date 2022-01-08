from django.shortcuts import render

from mainapp.models import Product, ProductCategory


def index(request):
    title = 'myShop'
    products = Product.objects.all()[:4]
    links_menu = ['домой', 'продукты', 'контакты',]
    context_page = {
        'title': title,
        'links_menu': links_menu,
        'products': products,
    }
    return render(request, 'myShop/index.html', context=context_page)


def contacts(request):
    title = 'контакты'
    links_menu = ['домой', 'продукты', 'контакты',]
    context_page = {
        'title': title,
        'links_menu': links_menu,
    }
    return render(request, 'myShop/contacts.html', context=context_page)
