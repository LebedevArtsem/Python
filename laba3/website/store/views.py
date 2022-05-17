from django.shortcuts import render

from .models import Product, User
from .forms import NewUser


def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})


def registration(request):
    if request.method == 'POST':
        pass
    else:
        form = NewUser()
    return render(request, 'store/registration.html', {'form': form})


def category(request):
    products = Product.objects.all()
    return render(request, 'store/category.html', {'products': products})
