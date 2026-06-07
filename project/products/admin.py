from django.contrib import admin

from .models import (
    Category, Product, ProductGroup, Size,
    ProductImage, ProductSizeStock,
    Activity, Fabric, Fit
)


class ProductSizeStockInline(admin.TabularInline):
    model = ProductSizeStock
    extra = 0
    min_num = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    ordering = ('order',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('group', 'color', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'group__category')
    search_fields = (
        'group__name',
        'color',
        'group__category__name',
    )
    list_editable = ('is_active',)
    exclude = ('slug',)

    inlines = [ProductImageInline, ProductSizeStockInline]


@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'fabric',
        'gender',
    )

    list_filter = (
        'category',
        'fabric',
        'gender',
        'activities',
    )

    search_fields = (
        'name',
        'category__name',
        'fabric__name',
    )

    filter_horizontal = (
        'sizes',
        'activities',
    )

    prepopulated_fields = {'slug': ('name', 'gender')}

    fields = (
        'name',
        'category',
        'fabric',
        'fit',
        'activities',
        'gender',
        'price',
        'sizes',
        'label',
        'features',
        'slug',
    )


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Fabric)
class FabricAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Fit)
class FitAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}