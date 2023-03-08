"""Модель User и менеджер модели User."""
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.core.exceptions import ValidationError


ROLE_CHOICE = (
    ('admin', 'admin'),
    ('user', 'user'),
    ('moderator', 'moderator'),
)


class UserManager(BaseUserManager):
    """Менеджер модели User"""

    def create_user(self, **kwargs):

        email = self.normalize_email(kwargs.get('email'))
        kwargs.pop('email', None)
        user = self.model(**kwargs)
        user.email = email
        user.save(using=self._db)

        return user

    def create_superuser(self, password=None, role='admin', **kwargs):

        email = self.normalize_email(kwargs.get('email'))
        kwargs.pop('email', None)
        user = self.create(**kwargs)
        user.set_password(None)
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


def validate_username(value):
    """Метод-валидатор запрещающий никнейм 'me'"""
    if value == 'me':
        raise ValidationError('Никнейм "me" запрещен.')


class User(AbstractBaseUser, PermissionsMixin):
    """Модель User."""
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    confirmation_code = models.CharField(max_length=7)
    bio = models.TextField(max_length=256, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICE,
        default='user',
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return self.username
