from django.urls import path
from back.views import UserViewSet, ProductViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = router.urls