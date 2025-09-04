from django.db import models
from students.models import Student
from subjects.models import Subject
from teachers.models import Teacher

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 89.50
    remarks = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "subject")
        ordering = ["student__user__last_name", "subject__name"]

    def __str__(self):
        return f"{self.student} - {self.subject} : {self.score}"
