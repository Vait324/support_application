from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        verbose_name='username',
        max_length=50,
        unique=True,
        help_text='Введите никнейм',
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
