from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from students.models import Student
from teachers.models import Teacher

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == "student":
            Student.objects.create(user=instance)
        elif instance.role == "teacher":
            Teacher.objects.create(user=instance)
