from django.views import generic as views

from project.products.models import Product


class ProductsListView(views.ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    GENDER_LABELS = {
        "women": "women's",
        "men": "wen's",
    }

    def get_queryset(self):
        return Product.objects.prefetch_related('images', 'group').filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']
        gender = self.request.GET.get('gender')
        product_type = self.request.GET.get('type')
        product_style = self.request.GET.get('style')

        extra_colors_dict = {}
        for product in products:
            variants = Product.objects.filter(group=product.group).exclude(pk=product.pk)
            extra_colors_dict[product.id] = list(variants)

        show_breadcrumbs = bool(product_type or product_style)

        context['extra_colors_dict'] = extra_colors_dict
        context['group_gender'] = gender
        context['group_gender_plural'] = self.GENDER_LABELS.get(gender, '')
        context['products_amount'] = products.count()
        context['product_type'] = product_type
        context['product_style'] = product_style
        context['show_breadcrumbs'] = show_breadcrumbs
        return context


class ProductDetailsView(views.DetailView):
    model = Product
    template_name = 'products/product_details.html'
    context_object_name = 'product_details'

    def get_queryset(self):
        return (
            Product.objects
            .select_related(
                'group',
            )
            .prefetch_related(
                'images',
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.object
        product_group = product.group

        recommendations = (
            product_group.styling_recommendations
            .select_related('target')
            .order_by('order')
        )

        context['variants'] = Product.objects.filter(group=self.object.group)
        context['current_variant'] = product

        context['recommendations'] = recommendations

        return context
