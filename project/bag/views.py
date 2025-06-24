from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic as views

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from project.bag.models import Bag, BagItem
from project.bag.serializers import BagItemSerializer
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

        items = bag.items.select_related('product', 'size')
        seen = {}

        for item in items:
            key = (item.product_id, item.size_id)
            if key in seen:
                seen[key].quantity += item.quantity
                seen[key].save()
                item.delete()
            else:
                seen[key] = item

        context['bag'] = bag
        context['items'] = bag.items.filter(quantity__gt=0).select_related('product', 'size')

        return context


class AddToBagView(APIView):
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        size_id = request.data.get('size_id')
        quantity = int(request.data.get('quantity', 1))

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

        bag_size = bag.items.aggregate(total=Sum('quantity'))['total'] or 0
        serializer = BagItemSerializer(item, context={'request': request})

        return Response({
            'bag_item': serializer.data,
            'bag_size': bag_size,
        }, status=status.HTTP_200_OK)


class RemoveFromBagView(APIView):
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        size_id = request.data.get('size_id')

        product = get_object_or_404(Product, id=product_id)
        size = get_object_or_404(Size, id=size_id)

        bag = authentication_check(request)

        try:
            item = BagItem.objects.get(
                bag=bag,
                product=product,
                size=size
            )

            if item.quantity > 1:
                item.quantity -= 1
                item.save()
                quantity = item.quantity
            else:
                item.delete()
                quantity = 0

            bag_size = bag.items.aggregate(total=Sum('quantity'))['total'] or 0

            return Response({
                'success': True,
                'bag_size': bag_size,
                'quantity': quantity
            }, status=status.HTTP_200_OK)

        except BagItem.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Item not found'
            }, status=status.HTTP_404_NOT_FOUND)


class IncreaseBagItemQuantity(APIView):
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        size_id = request.data.get('size_id')

        product = get_object_or_404(Product, id=product_id)
        size = get_object_or_404(Size, id=size_id)

        bag = authentication_check(request)

        try:
            item = BagItem.objects.get(
                bag=bag,
                product=product,
                size=size
            )

            item.quantity += 1
            item.save()
            quantity = item.quantity

            bag_size = bag.items.aggregate(total=Sum('quantity'))['total'] or 0

            return Response({
                'success': True,
                'bag_size': bag_size,
                'quantity': quantity
            }, status=status.HTTP_200_OK)
        except BagItem.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Item not found'
            }, status=status.HTTP_404_NOT_FOUND)
