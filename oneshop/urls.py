from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from accounts.views import GoogleLogin, kakao_login

schema_view = get_schema_view(
   openapi.Info(
      title="Oneshop API",
      default_version='v1',
      description="커머스 프로젝트 Oneshop의 API 문서입니다.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="jmpark6846@naver.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

swagger_apis = [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns = [
   path('admin/', admin.site.urls),

   # auth
   path('allauth/', include('allauth.urls')),
   path('accounts/', include('dj_rest_auth.urls')),
   path('accounts/registration/', include('dj_rest_auth.registration.urls')),

   # social login
   path('accounts/google/login/', GoogleLogin.as_view(), name="google_login"),
   path('accounts/kakao/login/', kakao_login, name='kakao_login'),

   # back app
   path('back/accounts/', include('back.urls')),
] + swagger_apis
