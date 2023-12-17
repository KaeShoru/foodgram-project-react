from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.apps import ApiConfig
from api.views import (
    ReceiptViewSet,
    TagViewSet,
    IngridientViewSet,
    FavoriteViewSet,
    ShoppingCartViewSet,
)
from users.views import (
    UserViewSet,
)


app_name = ApiConfig.name

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('receipes', ReceiptViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngridientViewSet, basename='ingredients')
router.register(r'favorites', FavoriteViewSet)
router.register(r'shopping_cart', ShoppingCartViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
