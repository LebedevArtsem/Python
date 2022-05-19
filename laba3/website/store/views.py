from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Product, Cart
from .forms import SignUpForm, SignInForm
from django.contrib.auth import login, logout


def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'store/registrate.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store')
    else:
        form = SignInForm()
    return render(request, 'store/login.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect('store')


def category(request):
    products = Product.objects.all()
    return render(request, 'store/category.html', {'products': products})


def get_product(request, product_id):
    item = Product.objects.get(pk=product_id)
    return render(request, 'store/product.html', {'item': item})


def cart(request):
    current_user = request.user
    products_cart = Cart.objects.filter(user_id=current_user.pk).values_list('product', flat=True)
    products = Product.objects.filter(pk__in=products_cart)
    return render(request, 'store/cart.html', {'products': products})


def add_to_cart(request, product_id):
    current_user = request.user
    Cart.objects.create(product_id=product_id, user_id=current_user.pk)
    return redirect('cart')


def clean_cart(request):
    current_user = request.user
    Cart.objects.filter(user_id=current_user.pk).delete()
    return redirect('cart')
