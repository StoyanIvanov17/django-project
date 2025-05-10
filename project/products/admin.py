from django.contrib import admin

from project.products import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'color', 'price', 'stock', 'category', 'group', 'created_at')
    list_filter = ('category', 'color', 'sizes', 'group', 'created_at', 'attribute_values')
    search_fields = ('title', 'description', 'color')
    prepopulated_fields = {"slug": ("title", "color")}
    autocomplete_fields = ['group', 'category', 'sizes']
    filter_horizontal = ('attribute_values',)


@admin.register(models.ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('parent__name', 'name')


@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    search_fields = ('product__title',)


@admin.register(models.ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    ordering = ('parent__name', 'name')


@admin.register(models.AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value')
    list_filter = ('attribute', 'applicable_categories')
    search_fields = ('value',)
    filter_horizontal = ('applicable_categories',)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    ordering = ('name',)