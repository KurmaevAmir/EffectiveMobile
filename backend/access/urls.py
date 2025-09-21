from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (RoleViewSet, BusinessElementViewSet, AccessRuleViewSet,
                    BusinessItemViewSet)

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'elements', BusinessElementViewSet, basename='element')
router.register(r'access-rules', AccessRuleViewSet, basename='access-rule')
router.register(r'items', BusinessItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),
]
