from django.urls import path

from .views import index, category, sign_in, sign_up, sign_out

urlpatterns = [
    path('', index, name='store'),
    path('registrate/', sign_up, name='registrate'),
    path('login/', sign_in, name='login'),
    path('logout/', sign_out, name='logout'),
    path('category', category, name='category'),
]
