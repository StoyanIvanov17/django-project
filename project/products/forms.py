from django import forms

from project.products.models import Product


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'subtitle', 'price', 'stock']