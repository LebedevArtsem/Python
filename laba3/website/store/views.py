from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, View

from .models import Product, Cart, Category
from .forms import SignUpForm, SignInForm
from django.contrib.auth import login, logout
import logging
from django.core.paginator import Paginator
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)


# async def index(request):
#     logger.info(request)
#     products = await sync_to_async(list)(Product.objects.all())
#     return render(request, 'store/index.html', {'products': products})


class IndexView(ListView):
    model = Product
    template_name = 'store/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()


# async def sign_up(request):
#     logger.info(request)
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = SignUpForm()
#     return render(request, 'store/registrate.html', {'form': form})


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'store/registrate.html'
    success_url = reverse_lazy('login')


# async def sign_in(request):
#     logger.info(request)
#     if request.method == 'POST':
#         form = SignInForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('store')
#     else:
#         form = SignInForm()
#     return render(request, 'store/login.html', {'form': form})


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


# async def sign_out(request):
#     logout(request)
#     logger.info(request)
#     return redirect('store')


class SignOutView(View):
    def get(self, request):
        logout(request)
        return redirect('store')


# async def category(request, category_id):
#     logger.info(request)
#     products = await sync_to_async(list)(Product.objects.filter(category_id=category_id).order_by('id'))
#     paginator = Paginator(products, 9)
#     page_num = request.GET.get('page', 1)
#     products_obj = paginator.get_page(page_num)
#     cat = await sync_to_async(Category.objects.get)(pk=category_id)
#     return render(request, 'store/category.html', {'products': products_obj, 'category': cat})


class CategoryView(ListView):
    model = Product
    template_name = 'store/category.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs['category_id'])


# async def get_product(request, product_id):
#     item = await sync_to_async(Product.objects.get)(pk=product_id)
#     cat = await sync_to_async(Category.objects.get)(pk=item.category_id)
#     logger.info(request)
#     return render(request, 'store/product.html', {'item': item, 'category': cat})


class ProductView(DetailView):
    template_name = 'store/product.html'
    model = Product
    context_object_name = 'item'
    pk_url_kwarg = 'product_id'


# def cart(request):
#     logger.info(request)
#     current_user = request.user
#     products_cart = (
#         Cart.objects.filter(user_id=current_user.pk).values_list('product', flat=True))
#     products = Product.objects.filter(pk__in=products_cart)
#     return render(request, 'store/cart.html', {'products': products})
#

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


async def add_to_cart(request, product_id):
    logger.info(request)
    current_user = request.user
    await sync_to_async(Cart.objects.create)(product_id=product_id, user_id=current_user.pk)
    return redirect('cart')


class AddToCartView(View):
    def get(self, request):
        current_user = request.user
        product_id = self.kwargs['product_id']
        Cart.objects.create(product_id=product_id, user_id=current_user.pk)
        return redirect('cart')


# async def clean_cart(request):
#     logger.info(request)
#     current_user = request.user
#     await sync_to_async(list)(Cart.objects.filter(user_id=current_user.pk).delete())
#     return redirect('cart')


class CleanCartView(View):
    def get(self, request):
        current_user = request.user
        Cart.objects.filter(user_id=current_user.pk).delete()
        return redirect('cart')


@login_required
def checkout(request):
    if request.method == 'POST':
        pass
    else:
        pass
    return render(request, 'store/checkout.html')


class CheckoutView(View):

    def get(self, request):
        pass

    def post(self, request):
        pass
