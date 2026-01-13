from django.views import generic as views

from project.products.models import Product


class ProductsListView(views.ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.prefetch_related('images', 'group').filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']

        extra_colors_dict = {}
        for product in products:
            variants = Product.objects.filter(group=product.group).exclude(pk=product.pk)
            extra_colors_dict[product.id] = list(variants)

        context['extra_colors_dict'] = extra_colors_dict
        return context


class ProductDetailsView(views.DetailView):
    model = Product
    template_name = 'products/product_details.html'
