from django.db import models
from django.contrib.auth.models import UserManager
from django.db import models
from django.utils import timezone
from django.conf import settings


from django.db import models
from django.conf import settings
from django.utils import timezone

class Note(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="classnotes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    fullName = models.CharField(max_length=75, blank=True, null=True)
    gradeSection = models.CharField(max_length=40, blank=True, null=True)
    completed = models.BooleanField(default=False)
    dateSubmitted = models.DateTimeField(default=timezone.now)

    DAMAGED_PROPERTY_CHOICES = [
        ('electricfan', 'Electric Fan'),
        ('outlet', 'Outlet'),
        ('tiles', 'Tiles'),
        ('television', 'Television'),
        ('window', 'Window'),
        ('whiteboard', 'Whiteboard'),
        ('chair', 'Chair'),
        ('table', 'Table'),
        ('other', 'Other'),
    ]

    # Priority based on importance
    PRIORITY_MAP = {
        'electricfan': 'High',
        'outlet': 'High',
        'tiles': 'High',
        'television': 'Medium',
        'window': 'Medium',
        'whiteboard': 'Medium',
        'chair': 'Low',
        'table': 'Low',
        'other': 'Low',
    }

    damagedProperty = models.CharField(
        max_length=5000,
        choices=DAMAGED_PROPERTY_CHOICES,
        blank=True,
        null=True,
        default=None
    )
    comment = models.TextField(blank=True, null=True)

    # 📸 Image upload field
    image = models.ImageField(upload_to='note_images/', null=True, blank=True)

    # 🏷️ Auto-generated priority tag
    priority = models.CharField(max_length=10, blank=True)

    def save(self, *args, **kwargs):
        # Auto-assign priority before saving
        if self.damagedProperty:
            self.priority = self.PRIORITY_MAP.get(self.damagedProperty, 'Low')
        else:
            self.priority = 'Low'
        super().save(*args, **kwargs)

    def __str__(self):
        if self.damagedProperty:
            return (
                f"{self.fullName or 'N/A'} ({self.gradeSection or 'N/A'}) - "
                f"Damaged Property: {self.damagedProperty}, Priority: {self.priority}, "
                f"Comment: {self.comment or 'No comment'}"
            )
        return f"Note by {self.fullName or 'Anonymous'}"


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None, section=None, **extra_fields):
        if not email:
            raise ValueError("Please provide a valid email address.")
        if not role:
            raise ValueError("Role is required.")

        email = self.normalize_email(email)

        # Auto-generate username
        if role.lower() == "adviser" and section:
            username = f"{section}-Adviser"
        elif role.lower() in ["engineer", "admin", "principal", "nurse", "librarian", "labtech", "utility"]:
            username = f"VCSMS-{role}"
        elif section:
            username = f"{section}-{role}"
        else:
            raise ValueError("Section is required for this role.")

        user = self.model(
            email=email,
            role=role,
            section=section,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, role="Admin", section=None, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=50)
    section = models.CharField(max_length=50, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def update_username(self):
        if self.role.lower() == "adviser" and self.section:
            self.username = f"{self.section}-Adviser"
        elif self.role.lower() in ["engineer", "admin", "principal", "nurse", "librarian", "labtech", "utility"]:
            self.username = f"VCSMS-{self.role}"
        elif self.section:
            self.username = f"{self.section}-{self.role}"
        else:
            raise ValueError("Section is required for this role.")
        self.save()
