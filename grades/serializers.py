from rest_framework import serializers
from .models import Grade

class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.get_full_name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.user.get_full_name", read_only=True)

    class Meta:
        model = Grade
        fields = ["id", "student", "student_name", "subject", "subject_name", "teacher_name", "score", "remarks", "created_at"]
