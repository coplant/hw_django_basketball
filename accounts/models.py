from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField("Имя пользователя", max_length=64, unique=True, null=True, blank=True)
    email = models.EmailField("Почта", unique=True, null=True, blank=True)
    phone_number = PhoneNumberField("Телефон", unique=True, null=True, blank=True)

    profile_image = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
