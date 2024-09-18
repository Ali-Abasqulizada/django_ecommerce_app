from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(
        verbose_name='Name',
        max_length=255
    )
    slug = models.SlugField(
        verbose_name='Slug',
        default='',
        unique=True
    )
    image = models.ImageField(
        verbose_name='Image',
        upload_to='category_images/',
        blank=True,
        null=True
    )
    product_count = models.PositiveIntegerField(
        verbose_name='Count of products',
        default=0
    )

    def __str__(self) -> str:
        return self.name
    
    def increase_product_count_by_one(self):
        self.product_count += 1
        self.save()

    def decrease_product_count_by_one(self):
        self.product_count -= 1
        self.save()

class Product(models.Model):
    name = models.CharField(
        verbose_name='Name',
        max_length=255
    )
    slug = models.SlugField(
        verbose_name='Slug',
        default='',
        unique=True
    )
    category = models.ForeignKey(
        verbose_name='Category',
        to=Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    description = models.TextField(
        verbose_name='Description'
    )
    price = models.DecimalField(
        verbose_name='Price',
        max_digits=7,
        decimal_places=2
    )
    discount_price = models.DecimalField(
        verbose_name='Discount Price',
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True
    )
    count = models.IntegerField(
        verbose_name='Stock Quantity'
    )
    available = models.BooleanField(
        verbose_name='Available',
        default=True
    )
    created_at = models.DateTimeField(
        verbose_name='Creation Time',
        auto_now_add=True
    )
    image = models.ImageField(
        verbose_name='Image',
        upload_to='product_images/'
    )
    average_rating = models.FloatField(
        verbose_name='Average Rating',
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    review_count = models.IntegerField(
        verbose_name='Review Count',
        default=0
    )

    change_category_count = models.BooleanField(
        verbose_name='Affect Category',
        default=True
    )

    def __str__(self) -> str:
        return f"'{self.name}' of '{self.category.name}' category"

class Cart(models.Model):
    user = models.ForeignKey(
        verbose_name='User',
        to=User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        verbose_name='Product',
        to=Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        verbose_name='Count',
        default=1
    )

    created_at = models.DateTimeField(
        verbose_name='Saved Time',
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f'{self.quantity} x {self.product.name} of {self.user.username}'

class Review(models.Model):
    user = models.ForeignKey(
        verbose_name='User',
        to=User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        verbose_name='Product',
        to=Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField(
        verbose_name='Rating',
        choices=[
            (1, '★☆☆☆☆'),
            (2, '★★☆☆☆'),
            (3, '★★★☆☆'),
            (4, '★★★★☆'),
            (5, '★★★★★')
        ]
    )

    comment = models.TextField(
        verbose_name='Comment',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        verbose_name='Review Time',
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f"Review of '{self.product.name}' by {self.user.username}"
