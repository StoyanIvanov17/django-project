from django.urls import reverse
from django.views import generic as views

from project.products.forms import ProductCreateForm
from project.products.models import Product


class ProductsListView(views.ListView):
    template_name = 'products/products.html'

    def get_queryset(self):
        return Product.objects.all()


class ProductCreateView(views.CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'products/product_create.html'

    def get_success_url(self):
        return reverse('product-details', kwargs={
            'pk': self.object.pk,
            'slug': self.object.slug
        })


class ProductDetailsView(views.DetailView):
    model = Product
    template_name = 'products/product_details.html'
