from django.urls import path

from .views import index, category, login, registrate

urlpatterns = [
    path('', index, name='store'),
    path('registrate/', registrate, name='registrate'),
    path('login/', login, name='login'),
    path('category', category, name='category'),
]
