from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import exceptions
from rest_framework.permissions import IsAdminUser
from accounts.models import User
from shop.models import Product, Image
from back.serializers import UserSerializer, ProductSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        image_files = request.FILES.getlist('image_files')

        try:
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            product = serializer.save()
            for file in image_files:
                Image.objects.create(
                    file=file,
                    product=product,
                )
            return Response(serializer.data, status=200)

        except exceptions.ValidationError as e:
            return Response(e.detail, status=e.status_code)

