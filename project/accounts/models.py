import uuid

from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import timezone

from project.accounts.managers import CustomUserManager


class CustomUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        max_length=30,
        unique=True,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )

    date_of_birth = models.DateField()

    date_joined = models.DateTimeField(
        default=timezone.now
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()


class Customer(models.Model):
    MAX_NAME_LENGTH = 20
    MAX_ADDRESS_LENGTH = 255
    MAX_PHONE_NUMBER_LENGTH = 20
    MAX_COUNTRY_NAME_LENGTH = 20

    first_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        null=True,
        blank=True,
        verbose_name='First Name'
    )

    last_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        null=True,
        blank=True,
        verbose_name='Last Name'
    )

    date_of_birth = models.DateField()

    phone_number = models.CharField(
        max_length=MAX_PHONE_NUMBER_LENGTH,
        null=True,
        blank=True,
        verbose_name='Phone Number'
    )

    country = models.CharField(
        max_length=MAX_COUNTRY_NAME_LENGTH,
        null=True,
        blank=True,
    )

    verified = models.BooleanField(
        default=False
    )

    verification_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    user = models.OneToOneField(
        CustomUser,
        primary_key=True,
        on_delete=models.CASCADE,
        unique=True,
    )
