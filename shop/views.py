import json
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import RetrieveAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from oneshop.permissions import IsOwnerOrReadOnly, IsOwner
from shop.exceptions import PaymentFailed
from shop.models import Product, Review, Cart, OrderItem, Order, Payment
from shop.payment import MockPaymentService
from shop.serializers import ProductListSerializer, ProductDetailSerializer, ReviewListCreateSerializer, \
    CartItemSerializer, CartSerializer, PaymentSerializer


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
            return Response(data={"error": "상품이 존재하지 않습니다."}, status=404)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return NotAuthenticated()

        product_id = self.kwargs['pk']
        try:
            product = Product.objects.get(id=product_id)
            serializer.save(product=product, user=self.request.user)
        except Product.DoesNotExist:
            return Response(data={"error": "상품이 존재하지 않습니다."}, status=404)


class ReviewView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListCreateSerializer
    permission_classes = [IsOwnerOrReadOnly]


@api_view(['POST'])
def add_to_cart(request: Request):
    if request.auth:
        cart = request.user.cart
    else:
        if 'cart_id' in request.COOKIES:
            cart = Cart.objects.get(id=request.COOKIES['cart_id'])
        else:
            cart = Cart()

    serializer = CartItemSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    serializer_data = serializer.data

    cart_items: dict = cart.to_dict
    product_id = serializer_data['product']

    if product_id in cart.to_dict:
        cart_items[product_id]['quantity'] += serializer_data['quantity']
    else:
        cart_items[product_id] = serializer_data

    cart.items = json.dumps(cart_items)
    cart.save()

    res = Response(data=CartSerializer(cart).data, status=201)
    if not request.auth and not ('cart_id' in request.COOKIES):
        expire = cart.created_at + timedelta(hours=1)
        res.set_cookie('cart_id', cart.id, expires=expire)

    return res

# TODO: delete cart item

@api_view(['GET'])
def get_cart(request):
    if request.auth:
        cart = request.user.cart
    elif 'cart_id' in request.COOKIES:
        cart = Cart.objects.get(id=request.COOKIES['cart_id'])
    else:
        return Response({}, 200)

    return Response(cart.to_dict, 200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    if request.user.cart.count == 0:
        return Response("장바구니가 비었습니다.", status=400)
    else:
        cart = request.user.cart.to_dict

        order = Order.objects.create(
            user=request.user,
        )
        for item in cart.values():
            OrderItem.objects.create(
                order=order,
                product_id=item['product'],
                quantity=item['quantity']
            )
        return Response({'order': order.id, 'status': order.status})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_payment(request):
    order_id = request.data.get('order', None)
    if not order_id:
        return Response("order_id not exists", status=400)

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response("order not exists", status=404)

    if order.user != request.user:
        return Response("not user's order", status=403)

    if order.status != Order.OrderStatus.NOT_PAID:
        return Response("Order already paid", status=400)

    data = {
        'payment_credential': order.user.id,
        'amount': order.total_price,
    }
    try:
        result = MockPaymentService.pay(data)
        payment = Payment.objects.create(
            user=order.user,
            order=order,
            amount=result['amount'],
            payment_id=result['payment_id']
        )

        return Response(PaymentSerializer(payment).data)
    except PaymentFailed as e:
        return Response(e.detail, status=e.status_code)
