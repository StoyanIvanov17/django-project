from django.views import generic as views

from project.products.models import Product


class HomeView(views.TemplateView):
    template_name = 'home/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        def get_product_with_last_image(group_slug):
            product = Product.objects.select_related('group').filter(
                group__slug=group_slug
            ).first()

            if product:
                product.last_extra_image = product.extra_images.order_by('-id').first()
            return product

        context['maxi_shirt'] = get_product_with_last_image('maxi-cotton-shirt-men')
        context['vinales_cotton_shorts'] = get_product_with_last_image('vinales-cotton-safari-short-men')
        context['boucle_knit_shirt'] = get_product_with_last_image('armando-cotton-boucle-knit-shirt-men')

        return context
