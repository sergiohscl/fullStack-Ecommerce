from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, null=True, default=''
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
