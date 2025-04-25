from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=100
    )

    slug = models.SlugField(
        unique=True
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=50
    )

    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(
        max_length=10
    )

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(
        max_length=50
    )

    hex_code = models.CharField(
        max_length=7,
        help_text="Hex code (e.g. #FFFFFF for white)"
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    name = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        unique=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    stock = models.PositiveIntegerField()

    image = models.ImageField(
        upload_to='product_images/'
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    sizes = models.ManyToManyField(
        Size, blank=True
    )

    colors = models.ManyToManyField(
        Color, blank=True
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True
    )

    def __str__(self):
        return self.name
