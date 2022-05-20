from django.shortcuts import render, redirect

from .models import Product, Cart, Category
from .forms import SignUpForm, SignInForm
from django.contrib.auth import login, logout
import logging
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)


def index(request):
    logger.debug(request)
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        logger.debug(request)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
        logger.debug(request)
    return render(request, 'store/registrate.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        logger.debug(request)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store')
    else:
        form = SignInForm()
        logger.debug(request)
    return render(request, 'store/login.html', {'form': form})


def sign_out(request):
    logout(request)
    logger.debug(request)
    return redirect('store')


def category(request, category_id):
    products = Product.objects.filter(category_id=category_id)
    logger.debug(request)
    paginator = Paginator(products, 9)
    page_num = request.GET.get('page', 1)
    products_obj = paginator.get_page(page_num)
    cat = Category.objects.get(pk=category_id)
    return render(request, 'store/category.html', {'products': products_obj, 'category': cat})


def get_product(request, product_id):
    item = Product.objects.get(pk=product_id)
    logger.debug(request)
    return render(request, 'store/product.html', {'item': item})


def cart(request):
    current_user = request.user
    products_cart = Cart.objects.filter(user_id=current_user.pk).values_list('product', flat=True)
    products = Product.objects.filter(pk__in=products_cart)
    logger.debug(request)
    return render(request, 'store/cart.html', {'products': products})


def add_to_cart(request, product_id):
    current_user = request.user
    Cart.objects.create(product_id=product_id, user_id=current_user.pk)
    logger.debug(request)
    return redirect('cart')


def clean_cart(request):
    current_user = request.user
    Cart.objects.filter(user_id=current_user.pk).delete()
    logger.debug(request)
    return redirect('cart')
