from datetime import timedelta

from django.db.models import Q, Exists, OuterRef
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

        return queryset.filter(query).distinct()

    def get_queryset(self):
        queryset = Product.objects.all()
        return self.filter_products(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_type_slugs = self.request.GET.getlist('item_type')
        item_type_value_slugs = self.request.GET.getlist('item_type_value')

        products = context['products']

        sizes = Size.objects.all().distinct()

        colors = Product.objects.values_list('color', flat=True).distinct()

        materials = Material.objects.all().distinct()

        attribute_values = AttributeValue.objects.filter(
            product__in=products
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
