from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, View

from .models import Product, Cart, Category
from .forms import SignUpForm, SignInForm, CheckoutForm
from django.contrib.auth import login, logout
import logging
from django.core.paginator import Paginator
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)


async def index(request):
    logger.info(request)
    products = await sync_to_async(list)(Product.objects.all())
    return render(request, 'store/index.html', {'products': products})


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
        form = self.form_class(data=self.request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class SignOutView(View):
    def get(self, request):
        logout(request)
        return redirect('store')


class CategoryView(View):
    model = Product
    template_name = 'store/category.html'

    def get(self, request, category_id):
        products = Product.objects.filter(category_id=category_id).order_by('id')
        paginator = Paginator(products, 9)
        page_num = request.GET.get('page', 1)
        products_obj = paginator.get_page(page_num)
        cat = Category.objects.get(pk=category_id)
        return render(request, self.template_name, {'products': products_obj, 'category': cat})


async def category(request, category_id):
    logger.info(request)
    products = await sync_to_async(list)(Product.objects.filter(category_id=category_id).order_by('id'))
    paginator = Paginator(products, 9)
    page_num = request.GET.get('page', 1)
    products_obj = paginator.get_page(page_num)
    cat = await sync_to_async(Category.objects.get)(pk=category_id)
    return render(request, 'store/category.html', {'products': products_obj, 'category': cat})


class ProductView(View):
    template_name = 'store/product.html'

    def get(self, request, product_id):
        item = Product.objects.get(pk=product_id)
        sizes = item.size
        return render(request, self.template_name, {'item': item, 'sizes': sizes})


async def get_product(request, product_id):
    item = Product.objects.get(pk=product_id)
    sizes = item.size
    return render(request, 'store/product.html', {'item': item, 'sizes': sizes})


class CartView(ListView):
    model = Product
    template_name = 'store/cart.html'
    context_object_name = 'products'

    def get_queryset(self):
        current_user = self.request.user
        products_cart = (
            Cart.objects.filter(user_id=current_user.pk).values_list('product', flat=True))
        return Product.objects.filter(pk__in=products_cart)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# async def add_to_cart(request, product_id):
#     logger.info(request)
#     current_user = request.user
#     await sync_to_async(Cart.objects.create)(product_id=product_id, user_id=current_user.pk)
#     return redirect('cart')


class AddToCartView(View):
    def get(self, request, product_id):
        current_user = request.user
        Cart.objects.create(product_id=product_id, user_id=current_user.pk)
        return redirect('cart')


class CleanCartView(View):
    def get(self, request):
        current_user = request.user
        Cart.objects.filter(user_id=current_user.pk).delete()
        return redirect('cart')


class CheckoutView(View):
    form_class = CheckoutForm
    template_name = 'store/checkout.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=self.request.POST)
        if form.is_valid():
            return redirect('store')
