from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=100
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        full_path = [self.name]
        parent = self.parent
        while parent is not None:
            full_path.append(parent.name)
            parent = parent.parent
        return ' > '.join(reversed(full_path))


class Size(models.Model):
    name = models.CharField(
        max_length=10
    )

    def __str__(self):
        return self.name


class ProductType(models.Model):
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


class ProductGroup(models.Model):
    name = models.CharField(
        max_length=255
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


class Product(models.Model):
    class Gender(models.TextChoices):
        MEN = 'men', 'Men'
        WOMEN = 'women', 'Women'
        UNISEX = 'unisex', 'Unisex'
        KIDS = 'kids', 'Kids'

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    extra_categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='additional_products'
    )

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name='products'
    )

    title = models.CharField(
        max_length=255
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices
    )

    group = models.ForeignKey(
        ProductGroup,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    sizes = models.ManyToManyField(
        Size, blank=True
    )

    color = models.CharField(
        max_length=50
    )

    video = models.FileField(
        upload_to='product_videos/',
        null=True,
        blank=True,
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    sale_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
    )

    stock = models.PositiveIntegerField()

    image = models.ImageField(
        upload_to='product_images/'
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
        unique=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_base = f"{self.title}-{self.color}"
            self.slug = slugify(slug_base)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.color}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='extra_images'
    )

    image = models.ImageField(
        upload_to='product_images/'
    )
