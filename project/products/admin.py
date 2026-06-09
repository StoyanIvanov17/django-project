from django.contrib import admin

from .models import (
    Category, Product, ProductGroup, Size,
    ProductImage, ProductSizeStock,
    Activity, Fabric, Fit
)


class ProductSizeStockInline(admin.TabularInline):
    model = ProductSizeStock
    extra = 0


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    ordering = ('order',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        sizes = list(Size.objects.all())

        if not change:
            ProductSizeStock.objects.bulk_create([
                ProductSizeStock(product=obj, size=size, stock=5)
                for size in sizes
            ])

    list_display = ('group', 'color', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'group__category')
    search_fields = (
        'group__name',
        'color',
        'group__category__name',
    )
    list_editable = ('is_active',)
    exclude = ('slug',)

    inlines = [ProductSizeStockInline, ProductImageInline]


@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'fabric',
        'fit',
        'gender',
        'price',
        'label',
    )

    list_filter = (
        'category',
        'fabric',
        'fit',
        'gender',
        'activities',
        'label',
    )

    search_fields = (
        'name',
        'category__name',
        'fabric__name',
        'fit__name',
    )

    filter_horizontal = (
        'sizes',
        'activities',
    )

    readonly_fields = ('slug',)

    fieldsets = (
        (
            'Basic Information',
            {
                'fields': (
                    'name',
                    'category',
                    'gender',
                    'label',
                    'price',
                )
            }
        ),
        (
            'Product Attributes',
            {
                'fields': (
                    'fabric',
                    'fit',
                    'activities',
                    'sizes',
                )
            }
        ),
        (
            'Product Details',
            {
                'fields': (
                    'features',
                    'sizing',
                    'materials_and_care',
                )
            }
        ),
        (
            'System',
            {
                'fields': ('slug',),
            }
        ),
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