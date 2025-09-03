from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, password=None, **extra_fields):
        if not first_name or not last_name:
            raise ValueError("Users must have a first and last name")

        if not extra_fields.get("is_superuser", False):
            username = f"{last_name.lower()}.{first_name.lower()}"
            extra_fields.setdefault("username", username)
            extra_fields.setdefault("role", CustomUser.STUDENT)

        user = self.model(first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields["role"] = None

        return self.create_user(first_name, last_name, password, **extra_fields)


class CustomUser(AbstractUser):
    STUDENT = "student"
    TEACHER = "teacher"
    MODERATOR = "moderator"

    ROLE_CHOICES = (
        (STUDENT, "Student"),
        (TEACHER, "Teacher"),
        (MODERATOR, "Moderator"),
    )

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True, unique=True)
    username = models.CharField(max_length=60, unique=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default="male")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.username} ({self.role if self.role else 'Superuser'})"
