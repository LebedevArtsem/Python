from django.urls import path

from .views import index, category, sign_in, sign_up, sign_out, get_product, cart, add_to_cart, clean_cart

urlpatterns = [
    path('', index, name='store'),
    path('registrate/', sign_up, name='registrate'),
    path('login/', sign_in, name='login'),
    path('logout/', sign_out, name='logout'),
    path('category/<int:category_id>/', category, name='category'),
    path('product/<int:product_id>/', get_product, name='product'),
    path('cart/', cart, name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('clean_cart', clean_cart, name='clean_cart'),
]
