from django.shortcuts import get_object_or_404
from django.views import generic as views

from project.products.models import Product, Category


class ProductsListView(views.ListView):
    template_name = 'products/products.html'

    def get_queryset(self):
        queryset = Product.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['products'] = self.get_queryset()

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


