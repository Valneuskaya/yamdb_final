from django.db import models
from django.contrib.auth.models import AbstractUser


CHOICES_USER_ROLE = (
    ('user', 'Аутентифицированный пользователь'),
    ('admin', 'Администратор'),
    ('moderator', 'Модератор')
)

USER = CHOICES_USER_ROLE[0][0]  # 'user'
ADMIN = CHOICES_USER_ROLE[1][0]  # 'admin'
MODERATOR = CHOICES_USER_ROLE[2][0]  # 'moderator'


class User(AbstractUser):
    email = models.EmailField(
        'email address', max_length=254, unique=True)
    bio = models.CharField(
        'Биография', max_length=200, blank=True)
    role = models.CharField(
        'Роль', max_length=20, choices=CHOICES_USER_ROLE,
        default='user', blank=True
    )

    def __str__(self):
        return str(self.username)
