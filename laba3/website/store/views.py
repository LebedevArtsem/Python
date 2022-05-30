import re

from django.contrib.auth.decorators import login_required
from django.core import validators, exceptions

from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, View

from .models import Product, Cart, Category
from .forms import SignUpForm, SignInForm, CheckoutForm, ProductForm
from django.contrib.auth import login, logout
import logging
from django.core.paginator import Paginator
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)


class IndexView(ListView):
    model = Product
    template_name = 'store/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'store/registrate.html'
    success_url = reverse_lazy('login')


class SignInView(View):
    form_class = SignInForm
    template_name = 'store/login.html'

    def post(self, request):
        logger.info(request)
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store')
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request):
        logger.info(request)
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class SignOutView(View):
    def get(self, request):
        logger.info(request)
        logout(request)
        return redirect('store')


class CategoryView(View):
    model = Product
    template_name = 'store/category.html'

    def get(self, request, category_id):
        logger.info(request)

        products = Product.objects.filter(category_id=category_id).order_by('id')

        paginator = Paginator(products, 9)
        page_num = request.GET.get('page', 1)
        products_obj = paginator.get_page(page_num)

        cat = Category.objects.get(pk=category_id)
        return render(request, self.template_name, {'products': products_obj, 'category': cat})


class ProductView(View):
    template_name = 'store/product.html'
    form_class = ProductForm

    def get(self, request, product_id):
        logger.info(request)
        item = Product.objects.get(pk=product_id)
        sizes = item.size
        return render(request, self.template_name, {'item': item, 'sizes': sizes})

    def post(self, request, product_id):
        logger.info(request)
        current_user = request.user
        size = request.POST['product_radio']
        try:
            order = Cart.objects.get(Q(product_id=product_id) & Q(product_size=size))
            order.quantity += 1
            order.save()
        except Cart.DoesNotExist:
            Cart.objects.create(product_id=product_id, user_id=current_user.pk, product_size=size)

        return redirect('cart')


class CartView(View):
    template_name = 'store/cart.html'

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        logger.info(request)
        current_user = request.user
        orders = Cart.objects.filter(user_id=current_user.pk)
        products_pk = orders.values_list('product', flat=True)

        products = []
        for i in products_pk:
            products.append(Product.objects.get(pk=i))

        orders_all = zip(range(1, orders.count() + 1), products, orders)

        logger.debug(request)
        return render(request, self.template_name, {'orders': orders_all})


class CleanCartView(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        logger.info(request)
        current_user = request.user
        Cart.objects.filter(user_id=current_user.pk).delete()
        return redirect('cart')


TOTAL_PRICE = 0


class CheckoutView(View):
    form_class = CheckoutForm
    template_name = 'store/checkout.html'

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        global TOTAL_PRICE
        TOTAL_PRICE = 0
        form = self.form_class()
        logger.info(request)
        orders = Cart.objects.filter(user_id=request.user.pk)
        products_pk = orders.values_list('product', flat=True)
        list = []
        for i in products_pk:
            list.append(Product.objects.get(pk=i))

        for order, product in zip(orders, list):
            TOTAL_PRICE += order.quantity * product.price

        return render(request, self.template_name, {'form': form, 'total_price': TOTAL_PRICE})

    def post(self, request):
        form = self.form_class(request.POST)
        global TOTAL_PRICE
        logger.info(request)

        if form.is_valid():
            return redirect('store')

        return render(request, self.template_name, {'form': form, 'total_price': TOTAL_PRICE})
