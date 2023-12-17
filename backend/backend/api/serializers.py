from rest_framework import serializers
from django.contrib.auth import authenticate
from djoser.serializers import UserCreateSerializer, UserSerializer

from users.models import User
from recipes.models import (
    RecipeIngredient,
    Recipe,
    Tag,
    Ingredient,
    Favorite,
    ShoppingCart
    )


class UsersSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
        )


class UsersCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'slug', 'measurement_unit')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='slug',
        read_only=False,
        many=True,
    )
    ingridients = RecipeIngredientSerializer(
        many=True,
        source='recipe_ingredient'
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'duration',
            'title',
            'description',
            'tags',
            'ingridients',
            'id',
        )


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=1, max_value=1000)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='slug',
        read_only=False,
        many=True,
    )
    ingridients = AddIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'author',
            'duration',
            'title',
            'description',
            'tags',
            'ingridients',
            'id',
        )


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if user:
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError('Incorrect email or password.')
