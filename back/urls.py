from django.urls import path
from back.views import UserViewSet, ProductViewSet,BackLoginView
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('login/', BackLoginView.as_view(), name='back-login'),
] + router.urls

