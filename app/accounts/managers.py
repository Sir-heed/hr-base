from django.contrib.auth.base_user import BaseUserManager
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from .choices import UserRole


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.role = UserRole.SUPER_ADMIN.value
        user.save(using=self._db)
        return user
