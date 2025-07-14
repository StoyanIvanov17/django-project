from datetime import timedelta

from django.db.models import Q, Exists, OuterRef, Max, Min
from django.utils.text import slugify
from django.utils.timezone import now
from django.views import generic as views

from project.products.models import Product, ItemType, Size, Material, AttributeValue, ProductGroup


class ProductsListView(views.ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def filter_products(self, queryset):
        category = self.request.GET.get('category', '')
        gender = self.request.GET.get('gender', '')
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

        if gender:
            query &= Q(group__gender=gender)

        if item_type_slugs:
            query &= Q(item_type__slug__in=item_type_slugs)

        if item_type_value_slug:
            query &= Q(item_type_value__slug=item_type_value_slug)

        if recent == 'true':
            query &= Q(created_at__gte=now() - timedelta(days=14))

        if sizes:
            query &= Q(size_stocks__size__name__in=sizes, size_stocks__stock__gte=1)

        if colors:
            query &= Q(color__in=colors)

        if materials:
            query &= Q(group__material_composition__material__name__in=materials)

        if min_price:
            query &= Q(group__price__gte=min_price)

        if max_price:
            query &= Q(group__price__lte=max_price)

        attribute_names_qs = AttributeValue.objects.filter(
            product_group__in=queryset.values_list('group_id', flat=True)
        ).values_list('attribute__name', flat=True).distinct()
        attributes_dict = {name for name in attribute_names_qs}

        slug_to_attr_name = {slugify(name): name for name in attributes_dict}

        excluded_params = ['category', 'item_type', 'item_type_value', 'recent', 'size', 'color', 'material',
                           'min_price', 'max_price']
        custom_attr_slugs = [
            key for key in self.request.GET.keys()
            if key not in excluded_params
        ]

        for attr_slug in custom_attr_slugs:
            original_attr_name = slug_to_attr_name.get(attr_slug)
            if not original_attr_name:
                continue

            selected_values = self.request.GET.getlist(attr_slug)
            if not selected_values:
                continue

            subquery = AttributeValue.objects.filter(
                product_group=OuterRef('group_id'),
                attribute__name__iexact=original_attr_name,
                value__in=selected_values
            )

            queryset = queryset.annotate(**{
                f'has_{attr_slug}': Exists(subquery)
            }).filter(**{
                f'has_{attr_slug}': True
            })

        return queryset.filter(query).distinct()

    def get_queryset(self):
        queryset = self.filter_products(Product.objects.all())
        return queryset.prefetch_related(
            'group__variants',
            'extra_images',
            'group__sizes',
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

        sizes = Size.objects.filter(
            product_stocks__product__in=base_queryset,
            product_stocks__stock__gte=1
        ).distinct()

        colors = base_queryset.values_list('color', flat=True).distinct()

        materials = Material.objects.all().distinct()

        attribute_values = AttributeValue.objects.filter(
            product_group__in=base_queryset.values_list('group_id', flat=True)
        ).select_related('attribute')

        attributes_dict = {}
        for av in attribute_values:
            attr_name = av.attribute.name
            if attr_name not in attributes_dict:
                attributes_dict[attr_name] = set()
            attributes_dict[attr_name].add(av.value)

        for key in attributes_dict:
            attributes_dict[key] = sorted(attributes_dict[key])

        gender_slug = self.request.GET.get('gender')
        category_slug = self.request.GET.get('category')

        product_filter = Q()
        if gender_slug:
            product_filter &= Q(group__gender=gender_slug)
        if category_slug:
            product_filter &= Q(category__slug=category_slug)

        item_types_with_products = ItemType.objects.annotate(
            has_products=Exists(
                Product.objects.filter(
                    item_type=OuterRef('pk')
                ).filter(product_filter)
            )
        ).filter(has_products=True)

        for item_type in item_types_with_products:
            item_type.filtered_values = item_type.values.annotate(
                has_products=Exists(
                    Product.objects.filter(
                        item_type_value=OuterRef('pk')
                    ).filter(product_filter)
                )
            ).filter(has_products=True)

        absolute_max_price = ProductGroup.objects.aggregate(Max('price'))['price__max'] or 0
        absolute_min_price = ProductGroup.objects.aggregate(Min('price'))['price__min'] or 0

        selected_min_price = self.request.GET.get('min_price') or absolute_min_price
        selected_max_price = self.request.GET.get('max_price') or absolute_max_price

        context['min_price'] = selected_min_price
        context['max_price'] = selected_max_price

        context['absolute_min_price'] = absolute_min_price
        context['absolute_max_price'] = absolute_max_price

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
        context['sizes'] = product.size_stocks.filter(stock__gt=0)
        return context
