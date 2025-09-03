#subjects/serializers.py
from rest_framework import serializers
from .models import Subject
from users.models import CustomUser


class SubjectSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role = "teacher"),
        required = False,
        allow_null = True
    )

    teacher_name = serializers.SerializerMethodField()
    student_names = serializers.SlugRelatedField(
        many=True,
        slug_field="username",
        read_only=True,
        source="students",
    )

    class Meta:
        model = Subject
        fields = [
            "id",
            "name",
            "code",
            "description",
            "teacher",
            "teacher_name",
            "students",
            "student_names",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["created_at", "students"]

    def get_teacher_name(self, obj):
        if obj.teacher:
            return f"{obj.teacher.first_name} {obj.teacher.last_name}"
        return None
