from rest_framework.serializers import ModelSerializer
from accounts.models import User
from shop.models import Product


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

