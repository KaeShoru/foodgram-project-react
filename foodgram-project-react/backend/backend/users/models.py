from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='Логин',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9_]+$',
            message="Логин может содержать только буквы, цифры и подчеркивания"
        )]
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
    )
    email = models.EmailField(
        max_length=100,
        verbose_name='email',
        unique=True
    )

    class Meta:
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username
