from django.shortcuts import render, redirect

from .models import Product
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
