from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=100
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ItemType(models.Model):
    name = models.CharField(
        max_length=100
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='item_types'
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ItemTypeValue(models.Model):
    item_type = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        related_name='values'
    )

    name = models.CharField(
        max_length=100
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(
        max_length=10
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductGroup(models.Model):
    class Gender(models.TextChoices):
        MEN = 'men', 'Men'
        WOMEN = 'women', 'Women'

    name = models.CharField(
        max_length=255,
        unique=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    description = models.TextField(
        blank=True
    )

    sizes = models.ManyToManyField(
        Size,
        blank=True,
        related_name='product_groups'
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='products'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = f"{self.name} {self.gender}"
            self.slug = slugify(base_slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    item_type = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        related_name='products_type'
    )

    item_type_value = models.ForeignKey(
        ItemTypeValue,
        on_delete=models.CASCADE,
        related_name='products_value'
    )

    group = models.ForeignKey(
        ProductGroup,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    color = models.CharField(
        max_length=50
    )

    color_hex = models.CharField(
        max_length=7
    )

    video = models.FileField(
        upload_to='product_videos/',
        null=True,
        blank=True
    )

    sale_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='product_images/'
    )

    model_size = models.CharField(
        max_length=50,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    is_active = models.BooleanField(
        default=True
    )

    slug = models.SlugField(
        unique=True, blank=True
    )

    def get_absolute_url(self):
        return reverse('product-details', kwargs={
            'pk': self.pk,
            'gender': self.group.gender,
            'slug': self.slug
        })

    def __str__(self):
        return f"{self.group.name} ({self.color})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = f"{self.group.name} {self.color}"
            slug_candidate = slugify(base_slug)
            counter = 1
            while Product.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = slugify(f"{base_slug} {counter}")
                counter += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='extra_images'
    )

    image = models.ImageField(
        upload_to='product_images/'
    )

    def __str__(self):
        return f"Image for {self.product}"


class Material(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class ProductMaterial(models.Model):
    product_group = models.ForeignKey(
        ProductGroup,
        on_delete=models.CASCADE,
        related_name='material_composition'
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
    )

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    class Meta:
        unique_together = ('product_group', 'material')

    def clean(self):
        if not self.product_group or not self.product_group.pk:
            return

        total = sum(
            pm.percentage for pm in ProductMaterial.objects.filter(product_group=self.product_group)
            if self.pk is None or pm.pk != self.pk
        )

        if total + self.percentage > 100:
            raise ValidationError(f"Total percentage for {self.product_group} exceeds 100%.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_group} - {self.material} ({self.percentage}%)"


class ProductAttribute(models.Model):
    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    product_group = models.ForeignKey(
        ProductGroup,
        on_delete=models.CASCADE,
        related_name='attribute_values'
    )

    attribute = models.ForeignKey(
        ProductAttribute,
        on_delete=models.CASCADE,
    )

    value = models.CharField(
        max_length=100
    )

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductSizeStock(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='size_stocks'
    )

    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        related_name='product_stocks'
    )

    stock = models.PositiveIntegerField()

    def clean(self):
        if self.size not in self.product.group.sizes.all():
            raise ValidationError(f"Size '{self.size}' is not valid for the product group '{self.product.group}'.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.size}: {self.stock}"
