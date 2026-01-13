from django.contrib import admin

from .models import (
    Category, Style, Product, ProductGroup, Size,
    ProductImage, ProductSizeStock, Type
)


class ProductSizeStockInline(admin.TabularInline):
    model = ProductSizeStock
    extra = 0
    min_num = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    ordering = ('-is_main', 'order')


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    show_change_link = True
    fields = (
        'category', 'style',
        'gender', 'tags', 'sizes',
        'color', 'color_hex',
        'video', 'price', 'sale_price',
        'stock', 'image', 'is_active'
    )
    inlines = [ProductImageInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('group', 'color', 'is_active')

    list_filter = ('is_active', )

    search_fields = (
        'title', 'tags__name')

    list_editable = ('is_active',)

    exclude = ('slug', )

    inlines = [ProductImageInline, ProductSizeStockInline]


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
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
    list_display = ('name', )

    prepopulated_fields = {'slug': ('name', 'gender')}

    search_fields = ('name',)

    fields = ('category', 'style', 'name', 'price', 'gender', 'sizes', 'slug',)


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)

    search_fields = ('name',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

    search_fields = ('name',)

    prepopulated_fields = {'slug': ('name',)}
