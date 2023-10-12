from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель просмотра, создания и удаления пользователей."""
    username = models.CharField(
        max_length=150,
        unique=True,
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username
