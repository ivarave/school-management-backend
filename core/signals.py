from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Student, Teacher

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            Student.objects.create(user=instance)
        elif instance.role == 'teacher':
            Teacher.objects.create(user=instance)
