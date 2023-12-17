from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from api.mixins import ListCreateDestroyMixin
from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeListSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
    CustomAuthTokenSerializer
)
from recipes.models import (
    Recipe, Tag, Ingredient, Favorite, ShoppingCart, Subscription
)


User = get_user_model()


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })


@api_view(['POST'])
def follow_user(request, user_id):
    user = request.user
    following_user = get_object_or_404(User, id=user_id)

    Subscription.objects.get_or_create(
        user=user, following_user=following_user
    )

    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def add_to_shopping_list(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)

    ShoppingCart.objects.get_or_create(user=user, recipe=recipe)

    return Response(status=status.HTTP_201_CREATED)


class TagViewSet(ListCreateDestroyMixin):
    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TagSerializer
    lookup_field = 'slug'
    search_fields = ('name',)


class IngridientViewSet(ListCreateDestroyMixin):
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]
    serializer_class = IngredientSerializer
    lookup_field = 'slug'
    search_fields = ('name',)


class ReceiptViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.action in ('list', 'retrive'):
            return RecipeListSerializer
        return RecipeSerializer

    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_id')
        return Recipe.reviews.filter(id=recipe_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=get_object_or_404(Recipe,
                                                id=self.kwargs.get
                                                ('recipe_id')))


class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class ShoppingCartViewSet(ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
