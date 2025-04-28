from django.views import generic as views

from project.products.models import Product


class ProductsListView(views.ListView):
    template_name = 'products/products.html'

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailsView(views.DetailView):
    model = Product
    template_name = 'products/product_details.html'
