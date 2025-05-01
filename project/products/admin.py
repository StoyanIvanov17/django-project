from django.contrib import admin
from .models import Product, Category, Size, ProductImage, ProductColor


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'category', 'created_at')
    list_filter = ('category', 'color', 'sizes', 'created_at')
    search_fields = ('title', 'subtitle', 'description')
    prepopulated_fields = {"slug": ("title", "subtitle")}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(ProductColor)
class ColorAdmin(admin.ModelAdmin):
    search_fields = ('name', 'hex_code')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    search_fields = ('product', 'alt_text')
