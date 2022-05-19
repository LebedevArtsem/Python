from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Product(models.Model):
    title = models.CharField(max_length=40, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    size = models.CharField(max_length=3, verbose_name='Размер')
    image = models.ImageField(upload_to='images', verbose_name='Изображение')
    rate = models.IntegerField(verbose_name='Рейтинг')
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        null=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_id': self.pk})

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'product_id': self.pk})

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Category(models.Model):
    title = models.CharField(max_length=10, verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Cart(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.PROTECT,
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True
    )

    def __str__(self):
        return "cart"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
