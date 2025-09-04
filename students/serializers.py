# students/serializers.py
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ["id", "username", "first_name", "last_name", "subjects"]

    def get_subjects(self, obj):
        # Use the related_name on CustomUser
        return [sub.name for sub in obj.user.subjects_enrolled.all()]
