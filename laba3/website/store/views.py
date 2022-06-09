from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, View

from .models import Product, Cart, Category
from .forms import SignUpForm, SignInForm, CheckoutForm, ProductForm
from django.contrib.auth import login, logout
import logging
from django.core.paginator import Paginator
from asgiref.sync import sync_to_async, async_to_sync
import asyncio
from django.core.mail import send_mail

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

        category_id = Product.objects.get(pk=product_id)
        str_to_redirect = f'/store/category/{category_id.category_id}/'

        return redirect(str_to_redirect)


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

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def send_mail_async(self, subj, msg, emails):
        send_mail(subj, msg, settings.EMAIL_HOST_USER, emails, fail_silently=False)
        a_send_mail = sync_to_async(send_mail)
        await a_send_mail(subj, msg, settings.EMAIL_HOST_USER, emails, fail_silently=False)

    # @method_decorator(login_required(login_url='login'))
    @sync_to_async
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

    async def post(self, request):
        form = self.form_class(request.POST)
        global TOTAL_PRICE
        logger.info(request)

        if form.is_valid():
            message = f'Hello, {request.user.username}, you have made a purchase for {TOTAL_PRICE}.'
            subject = 'Purchase in Esala Store'
            asyncio.create_task(self.send_mail_async(subject, message, [form.cleaned_data['email']]))
            return redirect('store')

        return render(request, self.template_name, {'form': form, 'total_price': TOTAL_PRICE})
