from datetime import timedelta

from django.db.models import Q
from django.utils.timezone import now
from django.views import generic as views

from project.products.models import Product, ItemType


class ProductsListView(views.ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def filter_products(self, queryset):
        category = self.request.GET.get('category', '')
        item_type_slugs = self.request.GET.getlist('item_type')
        item_type_value_slug = self.request.GET.get('item_type_value', '')
        recent = self.request.GET.get('recent', '')

        query = Q()

        if category:
            query &= Q(category__slug=category)

        if item_type_slugs:
            query &= Q(item_type__slug__in=item_type_slugs)

        if item_type_value_slug:
            query &= Q(item_type_value__slug=item_type_value_slug)

        if recent == 'true':
            query &= Q(created_at__gte=now() - timedelta(days=14))

        return queryset.filter(query)

    def get_queryset(self):
        queryset = Product.objects.all()
        return self.filter_products(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_type_slugs = self.request.GET.getlist('item_type')
        item_type_value_slugs = self.request.GET.getlist('item_type_value')

        context['item_type_slugs'] = item_type_slugs
        context['item_type_value_slugs'] = item_type_value_slugs
        context['all_item_types'] = ItemType.objects.all()

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
