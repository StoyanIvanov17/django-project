from datetime import timedelta

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views import generic as views

from project.products.models import Product, ItemType


class ProductsListView(views.ListView):
    template_name = 'products/products.html'

    def filter_products(self, queryset):
        category = self.request.GET.get('category', '')
        item_type_slug = self.request.GET.get('item_type', '')
        item_type_model_slug = self.request.GET.get('item_type_model', '')
        recent = self.request.GET.get('recent', '')

        query = Q()

        if category:
            query &= Q(category__slug=category)

        if item_type_slug:
            query &= Q(item_type__slug=item_type_slug)

        if item_type_model_slug:
            query &= Q(item_type_model__slug=item_type_model_slug)

        if recent == 'true':
            query &= Q(created_at__gte=now() - timedelta(days=14))

        return queryset.filter(query)

    def get_queryset(self):
        queryset = Product.objects.all()
        return self.filter_products(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        item_type_slug = self.request.GET.get('item_type', '')
        item_type = None
        item_type_models = []

        is_view_all = self.request.path == '/products/view-all/'

        if is_view_all:
            context['all_item_types'] = ItemType.objects.all()

        if item_type_slug:
            item_type = get_object_or_404(ItemType, slug=item_type_slug)
            item_type_models = item_type.specific_item_types.all()

        context['all_item_types'] = ItemType.objects.all()
        context['products'] = self.get_queryset()
        context['item_type'] = item_type
        context['item_type_models'] = item_type_models

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


