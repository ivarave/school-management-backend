#subjects/models.py
from django.db import models
from users.models import CustomUser
from teachers.models import Teacher
from students.models import Student


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "teacher"},
        related_name="subjects_taught",
    )

    students = models.ManyToManyField(
        CustomUser,
        blank=True,
        limit_choices_to={'role': 'student'},
        related_name="subjects_enrolled"
    )

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"
