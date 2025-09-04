# teachers/serializers.py
from rest_framework import serializers
from .models import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ["id", "user_id", "first_name", "last_name", "email", "phone", "is_active", "hired_date", "subjects"]

    def get_subjects(self, obj):
        # obj.user is the CustomUser related to this teacher
        return [sub.name for sub in obj.user.subjects_taught.all()]
