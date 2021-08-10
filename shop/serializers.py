from rest_framework.serializers import ModelSerializer

from shop.models import Product, Review


class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class ProductDetailSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class ReviewListCreateSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'title', 'content']

