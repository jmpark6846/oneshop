from rest_framework.generics import RetrieveAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response

from oneshop.permissions import IsOwnerOrReadOnly
from shop.models import Product, Review
from shop.serializers import ProductListSerializer, ProductDetailSerializer, ReviewListCreateSerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ReviewListCreateView(ListCreateAPIView):
    serializer_class = ReviewListCreateSerializer

    def get_queryset(self):
        product_id = self.kwargs['pk']
        try:
            product = Product.objects.get(id=product_id)
            reviews = Review.objects.filter(
                product=product
            )
            return reviews
        except Product.DoesNotExist:
            return Response(data={"error":"상품이 존재하지 않습니다."}, status=404)

    def perform_create(self, serializer):
        product_id = self.kwargs['pk']
        try:
            product = Product.objects.get(id=product_id)
            serializer.save(product=product)
        except Product.DoesNotExist:
            return Response(data={"error":"상품이 존재하지 않습니다."}, status=404)


class ReviewView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListCreateSerializer
    permission_classes = [IsOwnerOrReadOnly]
