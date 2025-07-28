from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from project.products.models import Category, ItemType, ItemTypeValue, Tag, ProductGroup, Product, ProductMaterial, \
    Material, Size, ProductSizeStock


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

        cls.product = Product.objects.create(
            category=cls.category,
            item_type=cls.item_type,
            item_type_value=cls.item_type_value,
            group=cls.product_group,
            color='Burgundy',
            color_hex='#800020',
        )

        cls.material = Material.objects.create(
            name='Cashmere'
        )

        cls.product_material = ProductMaterial.objects.create(
            product_group=cls.product_group,
            material=cls.material,
            percentage=Decimal('50')
        )


class CategoryTestCase(BaseProductTestCase):
    def test_category_slug_is_created_on_save(self):
        self.assertEqual(self.category.slug, 'clothing')

        category_two = Category.objects.create(name='Clothing New Arrivals')
        self.assertEqual(category_two.slug, 'clothing-new-arrivals')

    def test_category_without_name_raises_error(self):
        category = Category(name='')
        with self.assertRaises(ValidationError):
            category.full_clean()


class ItemTypeTestCase(BaseProductTestCase):
    def test_item_type_slug_is_created_on_save(self):
        self.assertEqual(self.item_type.slug, 'jeans')

    def test_deleting_category_deletes_item_type(self):
        self.category.delete()
        self.assertFalse(
            ItemType.objects.filter(
                pk=self.item_type.pk
            ).exists()
        )


class ItemTypeValueTestCase(BaseProductTestCase):
    def test_item_type_value_slug_is_created_on_save(self):
        self.assertEqual(self.item_type_value.slug, 'high-waist-jeans')

    def test_deleting_item_type_deletes_item_type_value(self):
        self.item_type.delete()
        self.assertFalse(
            ItemTypeValue.objects.filter(
                pk=self.item_type_value.pk
            ).exists()
        )


class TagTestCase(TestCase):
    def test_tag_slug_is_created_on_save(self):
        tag = Tag.objects.create(
            name='New Arrivals'
        )

        self.assertEqual(tag.slug, 'new-arrivals')


class ProductGroupTestCase(BaseProductTestCase):
    def test_product_group_slug_is_created_on_save(self):
        self.assertEqual(self.product_group.slug, 'high-waisted-skirt-women')


class ProductTestCase(BaseProductTestCase):
    def test_product_slug_is_created_on_save(self):
        self.assertEqual(self.product.slug, 'high-waisted-skirt-burgundy')

    def test_deleting_category_deletes_product(self):
        self.category.delete()
        self.assertFalse(
            Product.objects.filter(
                pk=self.product.pk
            ).exists()
        )

    def test_deleting_item_type_deletes_product(self):
        self.item_type.delete()
        self.assertFalse(
            Product.objects.filter(
                pk=self.product.pk
            ).exists()
        )

    def test_deleting_item_type_value_deletes_product(self):
        self.item_type_value.delete()
        self.assertFalse(
            Product.objects.filter(
                pk=self.product.pk
            ).exists()
        )

    def test_deleting_group_deletes_product(self):
        self.product_group.delete()
        self.assertFalse(
            Product.objects.filter(
                pk=self.product.pk
            ).exists()
        )

    def test_correct_product_get_absolute_url(self):
        expected_url = reverse('product-details', kwargs={
            'pk': self.product.pk,
            'gender': self.product_group.gender,
            'slug': self.product.slug
        })

        self.assertEqual(self.product.get_absolute_url(), expected_url)


class ProductMaterialTestCase(BaseProductTestCase):
    def test_product_material_percentage_raises_validation_error(self):
        material_2 = Material.objects.create(
            name='Cotton'
        )

        product_material_2 = ProductMaterial(
            product_group=self.product_group,
            material=material_2,
            percentage=Decimal('50.1')
        )

        with self.assertRaises(ValidationError) as context:
            product_material_2.clean()

        self.assertIn(
            f"Total percentage for {self.product_group} exceeds 100%.",
            str(context.exception)
        )


class ProductSizeStockTestCase(BaseProductTestCase):
    def test_product_size_stock_clean_method_raises_validation_error(self):
        size_xl = Size.objects.create(name='XL')

        size_stock = ProductSizeStock(
            product=self.product,
            size=size_xl,
            stock=5
        )

        with self.assertRaises(ValidationError) as context:
            size_stock.clean()

        self.assertIn(
            f"Size '{size_xl.name}' is not valid for the product group '{self.product_group}'.",
            str(context.exception)
        )