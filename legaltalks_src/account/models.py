from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

# Custom Manager
class AccountManager(BaseUserManager):
    def create_user(self, email, password, first_name, username, **other_fields):
        if not email:
            raise ValueError('You must provide an email address')
        if not username:
            raise ValueError('You must provide an username')
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            username = username,
            first_name = first_name,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, username, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')

        return self.create_user(email, password, first_name, username, **other_fields)

# Custom User Model
class Account(AbstractBaseUser, PermissionsMixin):
    email                       = models.EmailField(verbose_name='email', max_length=80, unique=True)
    username                    = models.CharField(max_length=30, unique=True)
    first_name                  = models.CharField(max_length=30)
    last_name                   = models.CharField(max_length=30)
    is_moderator                = models.BooleanField(default=False)
    is_advocate                 = models.BooleanField(default=False) # Toggle this field during registration
    is_verified                 = models.BooleanField(default=False)
    enrollment_no               = models.CharField(max_length=9, default=0)
    # Overriden Fields :
    is_active                   = models.BooleanField(default=True)
    is_staff                    = models.BooleanField(default=False)
    is_superuser                = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    objects = AccountManager()

    def __str__(self):
        return f'{self.username} {self.first_name}'


class ValidEnrollNo(models.Model):
    enrollment_no   = models.CharField(max_length=9, primary_key=True)
    advocate_email  = models.EmailField(max_length=80, unique=True)
    used            = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'ValidEnrollmtNo'

class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    gender = models.CharField(
        max_length = 1,
        choices = GENDER_CHOICES
    )
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_image = models.ImageField(default='default_user.jpg', upload_to='profile_pictures/')
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class CommonUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    gender = models.CharField(
        max_length = 1,
        choices = GENDER_CHOICES
    )
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_image = models.ImageField(default='default_user.jpg', upload_to='profile_pictures/')
    birth_date = models.DateField()

    def __str__(self):
        return f"Common user {self.user.username}'s profile"