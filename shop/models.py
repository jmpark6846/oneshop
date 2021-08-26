from enum import Enum
from functools import reduce
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
    order = models.SmallIntegerField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product.name}({self.order})'


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


class CartItem(models.Model):
    user = models.ForeignKey('accounts.User', related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.SmallIntegerField(default=1)


class Order(BaseModel):
    class OrderStatus(models.IntegerChoices):
        # 주문 상태는 간단히 두 가지만
        NOT_PAID = 0
        PAID = 1

    user = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING)
    status = models.SmallIntegerField(choices=OrderStatus.choices, default=OrderStatus.NOT_PAID)

    @property
    def total_quantity(self):
        return reduce(lambda total_quantity, item: total_quantity + item.price, self.items, 0)

    @property
    def total_price(self):
        return reduce(lambda total_price, item: total_price + item.price, self.items, 0)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.SmallIntegerField(default=0)

    @property
    def price(self):
        return self.product.price * self.quantity


class Cart(models.Model):
    user = models.ForeignKey('accounts.User', related_name='cart', on_delete=models.CASCADE)
    items = models.TextField()

