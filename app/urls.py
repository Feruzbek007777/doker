from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, LikeViewSet

router = DefaultRouter()
router.register('books', BookViewSet, basename='book')
router.register('likes', LikeViewSet, basename='like')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
