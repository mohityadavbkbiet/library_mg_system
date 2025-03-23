from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class AdminUserManager(BaseUserManager):
    """
    Custom manager for AdminUser with methods to create user and superuser.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with is_staff and is_superuser set to True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class AdminUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom Admin user model with email authentication.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True, null=True)  # New field for user profile details
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Fixing the reverse accessor clash with related_name.
    groups = models.ManyToManyField(
        Group,
        related_name='admin_users',  # Unique reverse name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='admin_users_permissions',  # Unique reverse name
        blank=True
    )

    objects = AdminUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Book(models.Model):
    """
    Model representing a book in the library.
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
