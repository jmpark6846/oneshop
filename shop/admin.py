from django.contrib import admin
from shop.models import Product, Review, Category, Image

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Image)