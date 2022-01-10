from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator


class UserProfileManager(BaseUserManager):
    """Manage for user profile"""

    def create_user(self, email, username, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('User must have a password')
        if not username:
            raise ValueError('User must have a username')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        print(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """Create and save a new superuser with given details"""
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('User must have a password')
        if not username:
            raise ValueError('User must have a username')
        email = self.normalize_email(email)
        user = self.create_user(email=email,
                                username=username,
                                password=password
                                )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True)
    CATEGORY = (
        ('Free', 'Free'),
        ('Low quality', 'Low quality'),
        ('Medium quality', 'Medium quality'),
        ('High quality', 'High quality'),
    )
    subscribe = models.CharField(
        max_length=50, choices=CATEGORY, default='Free')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserProfileManager()

    def __str__(self):
        """Retrieve full name of user"""
        return self.username


class Walpaper(models.Model):
    """Database model for wallpapers"""
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images', validators=[
                              FileExtensionValidator(allowed_extensions=['jpg', 'png'])])
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    CATEGORY = (
        ('Free', 'Free'),
        ('Low quality', 'Low quality'),
        ('Medium quality', 'Medium quality'),
        ('High quality', 'High quality'),
    )
    subscribe = models.CharField(
        max_length=50, choices=CATEGORY, default='Free')

    def __str__(self):
        """Retrieve full name of user"""
        return self.title
