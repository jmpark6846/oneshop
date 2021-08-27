from rest_framework import serializers
from accounts.models import User
from shop.models import Product, Review, Category, Image


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_staff', 'is_active']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'date_joined','last_login', 'is_staff', 'is_active']
        read_only_fields = ['id', 'email', 'password', 'date_joined', 'is_staff','last_login']


class ReviewSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    username = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'

    def get_username(self, review):
        return review.user.username


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    thumbnails = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'thumbnails']

    def get_thumbnails(self, product):
        serializer = ProductImageSerializer(product.images.order_by('order'), many=True)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = '__all__'

    def get_name(self, image):
        return image.file.name