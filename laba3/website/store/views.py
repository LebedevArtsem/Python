import asyncio

from django.shortcuts import render, redirect

from .models import Product, Cart, Category
from .forms import SignUpForm, SignInForm
from django.contrib.auth import login, logout
import logging
from django.core.paginator import Paginator
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)


async def index(request):
    logger.debug(request)
    products = await sync_to_async(list)(Product.objects.all())
    return render(request, 'store/index.html', {'products': products})


async def sign_up(request):
    logger.debug(request)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            asyncio.run(form.save())
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'store/registrate.html', {'form': form})


async def sign_in(request):
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


async def sign_out(request):
    logout(request)
    logger.debug(request)
    return redirect('store')


async def category(request, category_id):
    logger.debug(request)
    products = await sync_to_async(list)(Product.objects.filter(category_id=category_id).order_by('id'))
    paginator = Paginator(products, 9)
    page_num = request.GET.get('page', 1)
    products_obj = paginator.get_page(page_num)
    cat = await sync_to_async(Category.objects.get)(pk=category_id)
    return render(request, 'store/category.html', {'products': products_obj, 'category': cat})


async def get_product(request, product_id):
    item = await sync_to_async(Product.objects.get)(pk=product_id)
    logger.debug(request)
    return render(request, 'store/product.html', {'item': item})


async def cart(request):
    current_user = request.user
    products_cart = await sync_to_async(list)(
        Cart.objects.filter(user_id=current_user.pk).values_list('product', flat=True))
    products = await sync_to_async(Product.objects.filter)(pk__in=products_cart)
    logger.debug(request)
    return render(request, 'store/cart.html', {'products': products})


async def add_to_cart(request, product_id):
    current_user = request.user
    await sync_to_async(Cart.objects.create)(product_id=product_id, user_id=current_user.pk)
    logger.debug(request)
    return redirect('cart')


async def clean_cart(request):
    current_user = request.user
    await sync_to_async(list)(Cart.objects.filter(user_id=current_user.pk).delete())
    logger.debug(request)
    return redirect('cart')
