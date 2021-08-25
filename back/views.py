from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import exceptions
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from dj_rest_auth.views import LoginView
from accounts.models import User
from oneshop.paginations import DefaultPagination
from shop.models import Product, Image, Category, Review
from back.serializers import UserSerializer, ProductListSerializer, ProductDetailSerializer, CategorySerializer, \
    ReviewSerializer, UserCreateSerializer, ProductImageSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        else:
            return UserSerializer

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        user = self.get_object()
        reviews = Review.objects.filter(
            user=user
        )

        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        elif self.action == 'list':
            return ProductListSerializer
        elif self.action == 'update':
            return ProductDetailSerializer
        else:
            return ProductDetailSerializer

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        product = self.get_object()
        reviews = Review.objects.filter(
            product=product
        )

        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def thumbs(self, request, pk=None):
        image_files = request.FILES.getlist('image_files')
        product = self.get_object()
        image_count = product.images.count()
        try:
            for idx, file in enumerate(image_files, start=1):
                Image.objects.create(
                    file=file,
                    product=product,
                    order=image_count+idx
                )

            queryset = Image.objects.filter(
                product=product
            ).order_by('order')
            serializer = ProductImageSerializer(queryset, many=True)
            return Response(serializer.data, status=200)

        except exceptions.ValidationError as e:
            return Response(e.detail, status=e.status_code)

    @action(detail=True, methods=['put'])
    def set_order(self, request, pk=None):
        product = self.get_object()
        new_order_dict = self.request.data.get('order')
        queryset = Image.objects.filter(
            product=product
        )
        for thumb in queryset:
            thumb.order = new_order_dict[str(thumb.id)]
            thumb.save()

        ordered_thumbs = queryset.order_by('order')
        serializer = ProductImageSerializer(ordered_thumbs, many=True)
        return Response(serializer.data, status=200)
    

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all().order_by('created_at')
    serializer_class = ReviewSerializer


class BackLoginView(LoginView):
    permission_classes = (IsAdminUser, )