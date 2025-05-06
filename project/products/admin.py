from django.contrib import admin
from .models import Product, Category, Size, ProductImage, ProductType, ProductGroup


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'color', 'price', 'stock', 'category', 'group', 'created_at')
    list_filter = ('category', 'color', 'sizes', 'group', 'created_at')
    search_fields = ('title', 'description', 'color')
    prepopulated_fields = {"slug": ("title", "color")}
    autocomplete_fields = ['group', 'category', 'product_type', 'sizes']


@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


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


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    search_fields = ('product__title',)


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)

