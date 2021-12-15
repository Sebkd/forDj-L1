from django.shortcuts import render




def index(request):
    title = 'myShop'
    links_menu = ['домой', 'продукты', 'контакты',]
    context_page = {
        'title': title,
        'links_menu': links_menu,
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
