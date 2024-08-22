from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import BaseAbstractModel
from .choices import UserRole
from .managers import CustomUserManager


class User(BaseAbstractModel, AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=UserRole.choices(), default=UserRole.USER.value)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)
