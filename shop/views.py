import copy
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.generics import RetrieveUpdateDestroyAPIView


from shop.models import Product, Review
from shop.serializers import ProductListSerializer, ProductDetailSerializer, ReviewListCreateSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        product = self.get_object()
        queryset = Review.objects.filter(
            product=product,
        )
        serializer = ReviewListCreateSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reviews_create(self, request, pk=None):
        request_data = copy.deepcopy(request.data)
        request_data['product'] = pk
        serializer = ReviewListCreateSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class ReviewView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListCreateSerializer

    def get_object(self):
        review = super().get_object()
        if self.request.method != 'GET' and review.author != self.request.user :
            raise Exception()

        return review