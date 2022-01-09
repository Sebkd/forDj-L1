from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from authapp.forms import ShopUserRegisterForm

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser',
    '-is_staff', 'username')
    content = {
    'title': title,
    'objects': users_list
    }
    return render(request, 'adminapp/users.html', content)

@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/cоздание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {
    'title': title,
    'user_form': user_form
    }
    return render(request, 'adminapp/user_create.html', content)

@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    pass

@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    pass

@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'
    categories_list = ProductCategory.objects.all()
    context = {
    'title': title,
    'objects': categories_list
    }
    return render(request, 'adminapp/categories.html', context)

@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    pass

@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    pass

@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    pass

@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'
    category = get_object_or_404 (ProductCategory, pk = pk)
    products_list = Product.objects.filter (category__pk = pk).order_by ('name')
    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }
    return render (request, 'adminapp/products.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    pass

@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    pass

@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    pass

@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    pass
