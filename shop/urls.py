from django.urls import path

from shop.views import ProductListView, ProductDetailView, ReviewView, ReviewListCreateView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<pk>/reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<pk>/', ReviewView.as_view(), name='review-detail')
]
