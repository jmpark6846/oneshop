from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import exceptions
from rest_framework.permissions import IsAdminUser
from dj_rest_auth.views import LoginView
from accounts.models import User
from shop.models import Product, Image
from back.serializers import UserSerializer, ProductListSerializer, ProductDetailSerializer
from shop.serializers import ProductDetailSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'GET' and 'pk' in self.kwargs:
            return ProductDetailSerializer
        else:
            return ProductListSerializer

    def create(self, request, *args, **kwargs):
        image_files = request.FILES.getlist('image_files')
        try:
            serializer = ProductListSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            product = serializer.save()
            for file in image_files:
                Image.objects.create(
                    file=file,
                    product=product,
                )
            data = ProductDetailSerializer(product).data
            return Response(data, status=200)

        except exceptions.ValidationError as e:
            return Response(e.detail, status=e.status_code)


class BackLoginView(LoginView):
    permission_classes = (IsAdminUser, )