from django.shortcuts import render

from .models import Product
from .forms import SignUpForm
from django.views.generic import CreateView


def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})


def registrate(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SignUpForm()
    return render(request, 'store/registrate.html', {'form': form})


def login(request):
    return render(request, 'store/login.html')


def category(request):
    products = Product.objects.all()
    return render(request, 'store/category.html', {'products': products})
