from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=70)
    price = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)


class Category(models.Model):
    name = models.CharField(max_length=50)


class Review(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=120)
    content = models.TextField()