from rest_framework import serializers
from project.products.models import Product, Size, ProductGroup
from project.bag.models import BagItem


class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = ['name', 'price']


class ProductSerializer(serializers.ModelSerializer):
    group = ProductGroupSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['group', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['name']


class BagItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(
        read_only=True
    )

    size = SizeSerializer(
        read_only=True
    )

    class Meta:
        model = BagItem
        fields = ['product', 'size', 'quantity']
