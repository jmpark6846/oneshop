from django.urls import path
from rest_framework import routers
from shop.views import ProductListView, ProductDetailView, ReviewView, ReviewListCreateView, add_to_cart, place_order, \
    make_payment

# router = routers.SimpleRouter()
# router.register(r'cart', CartViewSet, basename='cart')

urls = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<pk>/reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<pk>/', ReviewView.as_view(), name='review-detail'),
    path('cart/', add_to_cart, name='add_to_cart'),
    path('cart/order/', place_order, name='place_order'),
    path('payment/', make_payment, name='make_payment')
]

urlpatterns = urls
