from django.contrib import admin

from .models import (
    Category, ItemType, ItemTypeValue, Product, ProductGroup, Tag, Size,
    ProductImage, ProductMaterial, Material, AttributeValue, ProductAttribute, ProductSizeStock
)


class ProductSizeStockInline(admin.TabularInline):
    model = ProductSizeStock
    extra = 0
    min_num = 1
    autocomplete_fields = ['size']


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1


class ProductMaterialInline(admin.TabularInline):
    model = ProductMaterial
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ItemTypeValueInline(admin.TabularInline):
    model = ItemTypeValue
    extra = 1


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    show_change_link = True
    fields = (
        'category', 'item_type', 'item_type_value',
        'gender', 'tags', 'sizes',
        'color', 'color_hex',
        'video', 'price', 'sale_price',
        'stock', 'image', 'is_active'
    )
    inlines = [ProductMaterialInline, ProductImageInline, AttributeValueInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'group', 'color', 'category', 'item_type',
        'item_type_value', 'is_active'
    )

    list_filter = (
        'category', 'item_type',
        'item_type_value', 'is_active'
    )

    search_fields = (
        'title', 'category__name', 'item_type__name',
        'item_type_value__name', 'tags__name'
    )

    list_editable = ('is_active',)

    exclude = ('slug', )

    inlines = [ProductImageInline, ProductSizeStockInline]


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)

    list_filter = ('category',)

    search_fields = ('name', 'category__name')

    prepopulated_fields = {'slug': ('name',)}


@admin.register(ItemTypeValue)
class ItemTypeValueAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type',)

    list_filter = ('item_type',)

    search_fields = ('name', 'item_type__name')

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

    inlines = [ProductMaterialInline, AttributeValueInline]

    fields = ('name', 'price', 'description', 'sizes', 'tags', 'gender', 'slug',)


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


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name',)

    search_fields = ('name',)
