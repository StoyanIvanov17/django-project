from django.contrib import admin
from .models import Product, Category, Size, ProductImage, ProductColor, ProductType


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'category', 'created_at')
    list_filter = ('category', 'color', 'sizes', 'created_at')
    search_fields = ('title', 'subtitle', 'description')
    prepopulated_fields = {"slug": ("title", "subtitle")}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('parent__name', 'name')


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(ProductColor)
class ColorAdmin(admin.ModelAdmin):
    search_fields = ('name', 'hex_code')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    search_fields = ('product', 'alt_text')


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )