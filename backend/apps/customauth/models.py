from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.text import slugify
import uuid
import secrets


class CustomUserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model using email for authentication."""

    USER_TYPE_CHOICES = (
        ('creator', 'Creator'),
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    )

    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='creator')
    slug = models.SlugField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'auth_customuser'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.email} {self.username}'

    def get_full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the user's short name."""
        return self.first_name

    def is_creator(self):
        """Check if user is a creator."""
        return self.user_type == 'creator'

    def is_admin_user(self):
        """Check if user is admin or staff."""
        return self.user_type in ['admin', 'staff']

    def save(self, *args, **kwargs):
        """
        Override save to auto-generate slug if not present from username. and
        replace spaces with hyphens in username.
        """
        if not self.slug:
            self.slug = slugify(self.username)
            self.slug = self.slug.lower()
        # Ensure username has no spaces
        self.username = self.username.replace(' ', '-').lower()
        super().save(*args, **kwargs)


class APIClient(models.Model):
    """Model for managing API clients (different frontends)."""

    CLIENT_TYPE_CHOICES = (
        ('web', 'Web Application'),
        ('mobile', 'Mobile Application'),
        ('internal', 'Internal Service'),
        ('partner', 'Partner API'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES)
    api_key = models.CharField(max_length=255, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    rate_limit = models.IntegerField(default=1000, help_text="Requests per hour")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auth_apiclient'
        verbose_name = 'API Client'
        verbose_name_plural = 'API Clients'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Generate API key if not present."""
        if not self.api_key:
            self.api_key = f"sk_{secrets.token_urlsafe(32)}"
        super().save(*args, **kwargs)

    def regenerate_api_key(self):
        """Regenerate the API key."""
        self.api_key = f"sk_{secrets.token_urlsafe(32)}"
        self.save()
