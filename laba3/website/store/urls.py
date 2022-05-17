from django.urls import path

from .views import index, registration, category

urlpatterns = [
    path('', index, name='store'),
    path('registration/', registration, name='registration'),
    path('category', category, name='category'),
]
