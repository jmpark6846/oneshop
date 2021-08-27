from rest_framework import serializers

from shop.models import Product, Review, Cart, Payment


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category']

    def validate_category(self, obj):
        return obj.name


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    reviews_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'reviews', 'reviews_count']
        depth = 2
        
    def validate_category(self, obj):
        return obj.name
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()


class ReviewListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'title', 'content']
        depth = 1
        read_only_fields = ['user','product']


class CartItemSerializer(serializers.Serializer):
    product = serializers.CharField()
    quantity = serializers.IntegerField()


class CartSerializer(serializers.Serializer):
    class Meta:
        model = Cart
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'