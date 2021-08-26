import json
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from oneshop.permissions import IsOwnerOrReadOnly, IsOwner
from shop.models import Product, Review
from shop.serializers import ProductListSerializer, ProductDetailSerializer, ReviewListCreateSerializer, \
    CartItemSerializer


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

            serializer.save(product=product, user=self.request.user)
        except Product.DoesNotExist:
            return Response(data={"error":"상품이 존재하지 않습니다."}, status=404)


class ReviewView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListCreateSerializer
    permission_classes = [IsOwnerOrReadOnly]


@api_view(['POST'])
def add_to_cart(self, request: Request):
    """
    카트 항목 추가
    post data validation, serialization
    cart json load
    check cart has product already
    if true:
        plus quantity in cart
    else:
        add new item to cart
    cart json dumps
    cart save
    """

    if request.user:
        serializer = CartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer_data = serializer.data
        cart = request.user.cart
        cart_items: dict = json.loads(cart.items)
        product_id = serializer_data['product']

        if product_id in cart_items:
            cart_items[product_id]['quantity'] += serializer_data['quantity']
        else:
            cart_items[product_id] = serializer_data

        cart.items = json.dumps(cart_items)
        cart.save()





#
#
# class CartViewSet(ModelViewSet):
#     # permission_classes = [IsOwner]
#
#     def get_queryset(self):
#         return self.request.user.cart
#
#     def get_serializer_class(self):
#         return CartItemSerializer
#
#     def create(self, request, *args, **kwargs):
#         """
#         카트 아이템 정보를 받고 아이템 생성
#         만약 이미 제품을 포함한 카트아이템이 있다면 갯수를 추가
#         """
#         if self.request.user:
#             serializer = CartItemSerializer(data=request.data)
#             if not serializer.is_valid():
#                 return Response(serializer.errors, status=400)
#
#             serializer_data = serializer.data
#             queryset = self.get_queryset().filter(
#                 product_id=serializer_data['product']
#             )
#
#             if queryset.exists():
#                 cart_item = queryset.all()[0]
#                 cart_item.quantity += serializer_data['quantity']
#                 cart_item.save()
#                 return Response(CartItemSerializer(cart_item).data)
#
#             return super(CartItemViewSet, self).create(request, *args, **kwargs)
#         else:
#             # 만약 로그인하지 않은 사용자도 카트를 추가할 수있어야함
#             # 카트 세션을 테이블에 만들고 쿠키에 세션 아이디 저장
#             pass