from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='store'),
    path('registrate/', SignUpView.as_view(), name='registrate'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category'),
    path('product/<int:product_id>/', ProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('clean_cart', CleanCartView.as_view(), name='clean_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
