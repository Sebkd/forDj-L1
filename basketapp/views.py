from django.shortcuts import render


def basket(request):
    context = {}
    return render(request, 'basketapp/basket.html', context)

def basket_add(request):
    pass

def basket_remove(request):
    pass

# Create your views here.
