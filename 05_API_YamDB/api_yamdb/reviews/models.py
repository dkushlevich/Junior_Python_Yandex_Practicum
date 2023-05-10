from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.validators import validate_username_not_me


class User(AbstractUser):
    ROLE_CHOICES = [
        ("user", "Аутентифицированнный пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Администратор"),
    ]

    bio = models.TextField(verbose_name="Биография", blank=True)
    email = models.EmailField(
        verbose_name="Email",
        max_length=254,
        unique=True
    )
    role = models.CharField(
        verbose_name="Роль",
        choices=ROLE_CHOICES,
        default="user",
        max_length=50
    )

    @property
    def is_admin(self):
        return (
            self.role == "admin" or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == "moderator"

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.get_username()

    def clean(self):
        validate_username_not_me(self.user)
        super().clean(self)
