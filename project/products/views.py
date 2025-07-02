from datetime import timedelta

from django.db.models import Q, Exists, OuterRef, Max, Min
from django.utils.text import slugify
from django.utils.timezone import now
from django.views import generic as views

from project.products.models import Product, ItemType, Size, Material, AttributeValue


class ProductsListView(views.ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def filter_products(self, queryset):
        category = self.request.GET.get('category', '')
        item_type_slugs = self.request.GET.getlist('item_type')
        item_type_value_slug = self.request.GET.get('item_type_value', '')

        recent = self.request.GET.get('recent', '')

        sizes = self.request.GET.getlist('size')
        colors = self.request.GET.getlist('color')
        materials = self.request.GET.getlist('material')

        max_price = self.request.GET.get('max_price')
        min_price = self.request.GET.get('min_price')

        query = Q()

        if category:
            query &= Q(category__slug=category)

        if item_type_slugs:
            query &= Q(item_type__slug__in=item_type_slugs)

        if item_type_value_slug:
            query &= Q(item_type_value__slug=item_type_value_slug)

        if recent == 'true':
            query &= Q(created_at__gte=now() - timedelta(days=14))

        if sizes:
            query &= Q(sizes__name__in=sizes)

        if colors:
            query &= Q(color__in=colors)

        if materials:
            query &= Q(material_composition__material__name__in=materials)

        if min_price:
            query &= Q(price__gte=min_price)

        if max_price:
            query &= Q(price__lte=max_price)

        for attr_name, values in self.request.GET.items():
            if attr_name in ['category', 'item_type', 'item_type_value', 'recent', 'size', 'color', 'material']:
                continue

            selected_values = self.request.GET.getlist(attr_name)
            if selected_values:
                query &= Q(attribute_values__attribute__name__iexact=attr_name) & Q(
                    attribute_values__value__in=selected_values)

        return queryset.filter(query).distinct()

    def get_queryset(self):
        queryset = self.filter_products(Product.objects.all())
        return queryset.prefetch_related(
            'group__variants',
            'extra_images',
            'sizes',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_type_slugs = self.request.GET.getlist('item_type')
        item_type_value_slugs = self.request.GET.getlist('item_type_value')
        products = context['products']

        base_queryset = Product.objects.all()

        category_slug = self.request.GET.get('category')
        if category_slug:
            base_queryset = base_queryset.filter(category__slug=category_slug)

        sizes = Size.objects.all().distinct()
        colors = base_queryset.values_list('color', flat=True).distinct()
        materials = Material.objects.all().distinct()

        attribute_values = AttributeValue.objects.filter(
            product__in=base_queryset
        ).select_related('attribute')

        attributes_dict = {}
        for av in attribute_values:
            attr_name = av.attribute.name
            if attr_name not in attributes_dict:
                attributes_dict[attr_name] = set()
            attributes_dict[attr_name].add(av.value)

        for key in attributes_dict:
            attributes_dict[key] = sorted(attributes_dict[key])

        item_types_with_products = ItemType.objects.annotate(
            has_products=Exists(
                Product.objects.filter(item_type=OuterRef('pk'))
            )
        ).filter(has_products=True)

        for item_type in item_types_with_products:
            item_type.filtered_values = item_type.values.annotate(
                has_products=Exists(
                    Product.objects.filter(item_type_value=OuterRef('pk'))
                )
            ).filter(has_products=True)

        context['max_price'] = Product.objects.aggregate(Max('price'))['price__max'] or 0
        context['min_price'] = Product.objects.aggregate(Min('price'))['price__min'] or 0

        context['sizes'] = sizes
        context['colors'] = colors
        context['materials'] = materials
        context['attributes'] = attributes_dict

        context['item_type_slugs'] = item_type_slugs
        context['item_type_value_slugs'] = item_type_value_slugs
        context['all_item_types'] = item_types_with_products

        context['selected_sizes'] = self.request.GET.getlist('size')
        context['selected_colors'] = self.request.GET.getlist('color')
        context['selected_materials'] = self.request.GET.getlist('material')

        selected_attributes = {}
        for attr_name in context['attributes']:
            param = self.request.GET.getlist(slugify(attr_name))
            if param:
                selected_attributes[attr_name] = param

        context['selected_attributes'] = selected_attributes

        extra_colors_dict = {}

        for product in products:
            group_variants = list(product.group.variants.all())
            variants_excluding_self = [v for v in group_variants if v.id != product.id]
            extra_colors_dict[product.id] = variants_excluding_self

        context['extra_colors_dict'] = extra_colors_dict

        return context


class ProductDetailsView(views.DetailView):
    model = Product
    template_name = 'products/product_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        color_variants = product.group.variants.exclude(id=product.id)

        context['extra_images'] = product.extra_images.all()
        context['extra_colors'] = color_variants
        context['sizes'] = product.sizes.all()

        return context
