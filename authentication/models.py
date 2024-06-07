from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from authentication.api.utils.create_confirmation_token import create_confirmation_token
import uuid

# Create your models here.


class MainUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        extra_fields.setdefault("activation_token", create_confirmation_token())
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, password, **extra_fields)


class Interest(models.Model):
    name = models.CharField(max_length=110, blank=False)

    def __str__(self):
        return self.name


class UserModel(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name="email",
        max_length=60,
        unique=True,
        error_messages={"unique": "This email already exists."},
    )
    password = models.CharField(max_length=120)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    account_confirmed = models.BooleanField(default=False)
    interests = models.ManyToManyField(Interest, blank=True)
    activation_token = models.CharField(max_length=90, blank=True, null=True)
    avatar = models.CharField(max_length=200, blank=True)
    account_type = models.CharField(
        max_length=30,
        default="basic",
        blank=True,
        choices=[
            ("basic", "basic"),
            ("premium", "premium"),
            ("enterprise", "enterprise"),
        ],
    )
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    retries = models.IntegerField(default=0)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]
    objects = MainUserManager()

    def __str__(self):
        return self.email
