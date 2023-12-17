from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ClassificatorModel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Адрес')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Tag(ClassificatorModel):
    class Meta:
        verbose_name = 'Тэг'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        unique_together = ('recipe', 'ingredient')


class Ingredient(ClassificatorModel):
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единицы измерения'
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        max_length=50,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=256, verbose_name='Название рецепта'
    )
    duration = models.DurationField(
        null=True,
        verbose_name='Время приготовления',
    )
    description = models.TextField(verbose_name='Описание рецепта')
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Тэги'
    )
    ingridients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Subscription(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
