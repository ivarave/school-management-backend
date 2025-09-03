from django.db import models
from users.models import CustomUser


class Moderator(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="moderator_profile"
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["user__last_name", "user__first_name"]

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name}"
