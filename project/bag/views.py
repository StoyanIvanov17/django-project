from django.shortcuts import get_object_or_404, redirect
from django.views import generic as views

from project.bag.models import Bag, BagItem
from project.products.models import Product, Size


def authentication_check(request):
    if request.user.is_authenticated:
        bag, _ = Bag.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key
        bag, _ = Bag.objects.get_or_create(session_key=session_key)
    return bag


class BagView(views.TemplateView):
    template_name = 'bag/bag.html'

    def get_bag(self):
        return authentication_check(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bag = self.get_bag()
        context['bag'] = bag
        context['items'] = bag.items.select_related('product')
        return context


class AddToBagView(views.View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        size_id = request.POST.get('size_id')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        size = get_object_or_404(Size, id=size_id)

        bag = authentication_check(request)

        item, created = BagItem.objects.get_or_create(
            bag=bag,
            product=product,
            size=size,
        )

        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        return redirect('bag')
