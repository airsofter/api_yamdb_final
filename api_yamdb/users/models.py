"""Модель User и менеджер модели User."""
from django.contrib.auth.models import (
    AbstractUser
)
from django.db import models


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICE = (
    (ADMIN, 'admin'),
    (USER, 'user'),
    (MODERATOR, 'moderator'),
)


class User(AbstractUser):
    """Модель User."""

    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    confirmation_code = models.CharField(max_length=7)
    bio = models.TextField(max_length=256, blank=True, null=True)
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICE,
        default=USER,
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username
