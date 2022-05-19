from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Product, Category, Cart


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category')
    list_display_links = ('id', 'title')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Product, ProductAdmin)

admin.site.register(Category, CategoryAdmin)

admin.site.register(Cart)
