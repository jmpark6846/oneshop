from django.urls import path, include
from rest_framework.routers import SimpleRouter
from shop.views import ProductViewSet, ReviewView

router = SimpleRouter()
router.register('product', ProductViewSet)


urlpatterns = [
    path('reviews/<pk>/', ReviewView.as_view(), name='review')
] + router.urls