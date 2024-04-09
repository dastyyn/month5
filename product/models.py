from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="product_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="product_user_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField(max_length=300)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stars = models.DecimalField(max_digits=3, decimal_places=1, default=1)

    def __str__(self):
        return self.text
