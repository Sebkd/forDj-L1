from django.shortcuts import render


def index(request):
    return render(request, 'myShop/index.html')


def contacts(request):
    return render(request, 'myShop/contacts.html')
