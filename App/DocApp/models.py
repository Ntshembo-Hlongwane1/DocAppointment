from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):

  def create_user(self, email, user_name, first_name, password, **other_fields):
    
    if not email:
      raise ValidationError('Email is required')

    email = self.normalize_email(email)
    user = self.model(email=email, user_name=user_name, first_name=first_name, **other_fields)
    user.set_password(password)
    user.save()
    return user

  def create_superuser(self, email, user_name, first_name, password, **other_fields):
    other_fields.setdefault('is_staff', True)
    other_fields.setdefault('is_active', True)
    other_fields.setdefault('is_superuser', True)

    return self.create_user(email, user_name, first_name, password, **other_fields)

class Person(AbstractBaseUser, PermissionsMixin):

  email = models.EmailField(_('Email Address'), unique=True)
  user_name = models.CharField(max_length=150, unique=True)
  first_name = models.CharField(max_length=150)

  objects  = UserManager()

  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['user_name', 'first_name']

  def __str__(self):
    return self.email