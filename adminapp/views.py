from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser',
    '-is_staff', 'username')
    context = {
    'title': title,
    'objects': users_list
    }
    return render(request, 'adminapp/users.html', context)

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

    context = {
    'title': title,
    'user_or_edit_form': user_form
    }
    return render(request, 'adminapp/user_create.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:user_update', args = [edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    context = {
    'title': title,
    'user_or_edit_form': edit_form,
    }
    return render(request, 'adminapp/user_create.html', context)

@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'

    _user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        _user.is_active = False
        _user.save()
        return HttpResponseRedirect(reverse('admin_staff:users'))
    context = {
    'title': title,
    'user_to_delete': _user,
    }
    return render(request, 'adminapp/user_delete.html', context)

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
    title = 'категории/удаление'

    _category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        _category.is_active = False
        _category.save()
        return HttpResponseRedirect(reverse('admin_staff:categories'))
    context = {
    'title': title,
    'category_to_delete': _category,
    }
    return render(request, 'adminapp/category_delete.html', context)

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
    title = 'продукт/cоздание'

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin_staff:products', args = [pk]))
    else:
        product_form = ProductEditForm(initial = {'category': category})

    context = {
    'title': title,
    'update_form': product_form,
    }
    return render(request, 'adminapp/product_update.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = 'продукт/подробнее'

    product = get_object_or_404 (Product, pk = pk)

    context = {
        'title': title,
        'object': product,
    }
    return render (request, 'adminapp/product_read.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance = edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:products',
                                                args = [edit_product.category.pk]))
    else:
        edit_form = ProductEditForm(instance = edit_product)

    context = {
    'title': title,
    'update_form': edit_form,
    'category': edit_product.category
    }
    return render(request, 'adminapp/product_update.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт/удаление'

    delete_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        delete_product.is_active = False
        delete_product.save()
        return HttpResponseRedirect(reverse('admin_staff:products', args = [delete_product.category.pk]))
    context = {
    'title': title,
    'product_to_delete': delete_product,
    }
    return render(request, 'adminapp/product_delete.html', context)
