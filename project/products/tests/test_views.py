from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile


from project.products.models import Category, ItemType, ItemTypeValue, Tag, ProductGroup, Product, ProductMaterial, \
    Material, Size


class BaseProductTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name='Clothing'
        )

        cls.item_type = ItemType.objects.create(
            name='Jeans',
            category=cls.category
        )

        cls.item_type_value = ItemTypeValue.objects.create(
            item_type=cls.item_type,
            name='High Waist Jeans'
        )

        cls.product_group = ProductGroup.objects.create(
            name='High Waisted Skirt',
            gender=ProductGroup.Gender.WOMEN,
            price=59.99,
            description='',
        )

        cls.size_s = Size.objects.create(name='S')
        cls.size_m = Size.objects.create(name='M')
        cls.size_l = Size.objects.create(name='L')

        cls.product_group.sizes.set([
            cls.size_s,
            cls.size_m,
            cls.size_l
        ])

        cls.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/gif'
        )

        cls.product = Product.objects.create(
            category=cls.category,
            item_type=cls.item_type,
            item_type_value=cls.item_type_value,
            group=cls.product_group,
            color='Burgundy',
            color_hex='#800020',
            image=cls.image,
        )

        cls.material = Material.objects.create(
            name='Cashmere'
        )

        cls.product_material = ProductMaterial.objects.create(
            product_group=cls.product_group,
            material=cls.material,
            percentage=Decimal('50')
        )

    def test_get_response(self, params=None):
        url = reverse('all-products')
        return self.client.get(url, params or {})

    def test_status_code_200(self):
        response = self.test_get_response()
        self.assertEqual(response.status_code, 200)

    def test_products_loaded(self):
        response = self.test_get_response()
        print(response.context.keys())
        self.assertIn(self.product, response.context['products'])

    def test_filter_by_category(self):
        response = self.test_get_response({'category': 'clothing'})
        self.assertIn(self.product, response.context['products'])

    def test_filter_by_gender(self):
        response = self.test_get_response({'gender': 'women'})
        self.assertIn(self.product, response.context['products'])

    def test_filter_by_item_type_slug(self):
        response = self.test_get_response({'item_type_slug': 'jeans'})
        self.assertIn(self.product, response.context['products'])

    def test_filter_by_item_type_value_slug(self):
        response = self.test_get_response({'item_type_value_slug': 'high-waist-jeans'})
        self.assertIn(self.product, response.context['products'])

    def test_filter_by_size(self):
        response = self.test_get_response({'sizes': ['M']})
        self.assertIn(self.product, response.context['products'])

    def test_materials(self):
        response = self.test_get_response({'materials': ['Cashmere']})
        self.assertIn(self.product, response.context['products'])

