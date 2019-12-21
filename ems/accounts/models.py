from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Account(models.Model):
    name            =   models.CharField(blank=False,max_length=256,help_text="enter name")
    email           =   models.EmailField(blank=False,help_text="enter email")
    password        =   models.CharField(blank=False,max_length=256,help_text="password",default="pass")
    phone           =   PhoneNumberField(blank=False,help_text="enter phone number")
    account_type    =   models.CharField(blank=False,max_length=7,help_text="visitor or host")

    def __str__(self):
        return self.name

class Meeting(models.Model):
    visitor_name    =   models.CharField(blank=False,max_length=256)
    visitor_phone   =   PhoneNumberField()
    host_id         =   models.CharField(blank=False,max_length=500)
    check_in_time   =   models.TimeField()
    check_out_time  =   models.TimeField()
    timestamp       =   models.DateTimeField()
    address         =   models.CharField(blank=False,max_length=1000)

    def __str__(self):
        return self.visitor_name
    
    