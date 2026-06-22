from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Activity(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    featured_on_homepage = models.BooleanField(
        default=False
    )

    homepage_description = models.TextField(
        blank=True
    )

    homepage_image = models.ImageField(
        upload_to='homepage_categories/',
    )

    homepage_order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        verbose_name_plural = 'Activities'
        ordering = ['homepage_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Fabric(models.Model):
    name = models.CharField(
        max_length=100,
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


class Fit(models.Model):
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


class Category(models.Model):
    name = models.CharField(
        max_length=50
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
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Size(models.Model):
    name = models.CharField(
        max_length=10
    )

    def __str__(self):
        return self.name


class ProductLabel(models.TextChoices):
    NEW = "new", "New Arrival"
    LIMITED = "limited", "Limited Edition"
    SALE = "sale", "On Sale"
    TRENDING = "trending", "Trending"


class ProductGroup(models.Model):
    class Gender(models.TextChoices):
        MEN = 'men', 'Men'
        WOMEN = 'women', 'Women'

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    fabric = models.ForeignKey(
        Fabric,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    fit = models.ForeignKey(
        Fit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    activities = models.ManyToManyField(
        Activity,
        blank=True,
        related_name='products'
    )

    name = models.CharField(
        max_length=255,
        unique=True
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    sizes = models.ManyToManyField(
        Size,
        blank=True,
        related_name='product_groups'
    )

    label = models.CharField(
        max_length=20,
        choices=ProductLabel.choices,
        blank=True,
        null=True
    )

    features = models.TextField(
        blank=True,
        help_text="One feature per line."
    )

    sizing = models.TextField(
        blank=True
    )

    materials_and_care = models.TextField(
        blank=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.gender}")
            slug = base_slug
            counter = 1

            while ProductGroup.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class StylingRecommendation(models.Model):
    source = models.ForeignKey(
        ProductGroup,
        on_delete=models.CASCADE,
        related_name='styling_recommendations'
    )

    target = models.ForeignKey(
        ProductGroup,
        on_delete=models.CASCADE,
        related_name='+'
    )

    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['order']
        unique_together = ('source', 'target')

    def __str__(self):
        return f"{self.source} → {self.target}"


class Product(models.Model):
    group = models.ForeignKey(
        ProductGroup,
        on_delete=models.CASCADE,
        related_name='product_variants'
    )

    color = models.CharField(
        max_length=50
    )

    color_hexes = models.CharField(
        max_length=50
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
        blank=True
    )

    sale_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True
    )

    def get_absolute_url(self):
        return reverse(
            'product-details',
            kwargs={
                'pk': self.pk,
                'gender': self.group.gender,
                'slug': self.slug
            }
        )

    def __str__(self):
        return f"{self.group.name} ({self.color})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.group.name}-{self.color}")
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    @property
    def main_image(self):
        return self.images.filter(
            is_main=True
        ).first() or self.images.first()

    @property
    def available_sizes(self):
        return (
            self.size_stocks
            .filter(stock__gt=0)
            .select_related('size')
        )


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='product_images/',
        max_length=1000
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_main = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.product}"

    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(
                product=self.product,
                is_main=True
            ).exclude(
                pk=self.pk
            ).update(
                is_main=False
            )

        super().save(*args, **kwargs)


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

    class Meta:
        unique_together = ('product', 'size')

    def __str__(self):
        return f"{self.product} - {self.size}: {self.stock}"

