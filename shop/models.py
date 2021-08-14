from django.db import models

from oneshop.models import BaseModel


class Product(models.Model):
    name = models.CharField(max_length=70)
    price = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Image(models.Model):
    file = models.ImageField(null=False)
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Review(BaseModel):
    user = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=120)
    content = models.TextField()

    def __str__(self):
        return f'{self.product.name} - {self.title}'