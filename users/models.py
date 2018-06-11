from decimal import Decimal

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MinValueValidator
from django.utils.crypto import get_random_string

from .countries import COUNTRY_CHOICES


def make_activation_code():
    """ Generate a unique activation code. """

    # Use Django's crypto get_random_string() instead of rolling our own.
    return get_random_string(length=40)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):

    STATUS_REGISTERED = 1
    STATUS_PENDING = 2
    STATUS_UNCONFIRMED = 3
    STATUS_CHOICES = (
        (STATUS_REGISTERED, 'Registered'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_UNCONFIRMED, 'Unconfirmed')
    )


    email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    eth_address = models.CharField(max_length=42, unique=True, null=True, blank=True)
    eth_amount = models.DecimalField(
        max_digits=20, decimal_places=10, default=Decimal('0.1'),
        validators=[MinValueValidator(Decimal('0.1'), message="ETH amount should minimum 0.1")]
    )
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
                                            default=STATUS_PENDING)
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default='canada')
    editable = models.BooleanField(default=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


    def username(self):
        username = self.email.split('@')[0]
        return username


class Subscription(models.Model):
    email = models.EmailField(verbose_name='email address',
                              max_length=255, unique=True)
    unsubscribed = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=40,
                                       default=make_activation_code)
