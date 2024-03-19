from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserType(models.TextChoices):
    ADMINISTRATOR = "Admin"
    USER = "User"


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=200, default="", blank=True)
    last_name = models.CharField(max_length=200, default="", blank=True)
    email = models.EmailField(unique=True, db_index=True)
    user_type = models.CharField(max_length=15, choices=UserType.choices)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = BaseUserManager()
