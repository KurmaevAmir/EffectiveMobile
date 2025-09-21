from django.urls import path, include
from .views import CustomUserViewSet, ProfileViewSet, LogoutView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'me', ProfileViewSet, basename='me')


urlpatterns = [
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include(router.urls)),
    path('auth/', include('djoser.urls')),
]
