from django.contrib import admin
from django.template.defaultfilters import slugify

from .models import Category, ItemType, ItemTypeModel, Product, ProductGroup, Tag, Size, ProductImage, ProductAttribute, AttributeValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'item_type', 'item_type_model', 'price', 'stock', 'is_active')
    list_filter = ('category', 'item_type', 'item_type_model', 'gender', 'tags', 'is_active')
    search_fields = ('title', 'category__name', 'item_type__name', 'item_type_model__name', 'tags__name')
    list_editable = ('is_active', 'price')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ItemTypeModel)
class ItemTypeModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type',)
    list_filter = ('item_type',)
    search_fields = ('name', 'item_type__name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value')
    list_filter = ('attribute',)
    search_fields = ('attribute__name', 'value')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image',)