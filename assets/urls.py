from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssetViewSet, run_checks
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Asset API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'assets', AssetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('run-checks/', run_checks),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
