from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Teacher, Subject, Grade, ClassRoom, Timetable, Attendance, classAttendance, CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

class TeacherInfoSerializer(serializers.ModelSerializer):
    # Include related user fields
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = Teacher
        fields = [
            'id',
            'teacher_id',
            'first_name',
            'last_name',
            'username',
            'email',
            'role',
            'name',      # model-specific field
            'age',       # model-specific field
        ]

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'password', 'is_approved')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'role']

class TeacherSerializer(serializers.ModelSerializer):
    # Include related user fields
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = Teacher
        fields = [
            'id',
            'teacher_id',
            'first_name',
            'last_name',
            'username',
            'email',
            'role',
            'name',
            'age',
        ]

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'

class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class ClassAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = classAttendance
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        role = attrs.get('role')
        allowed_roles = ['student', 'teacher', 'moderator']
        if role not in allowed_roles:
            raise serializers.ValidationError("Role must be either 'student', 'teacher', or 'moderator'")
        return attrs

    def create(self, validated_data):
        role = validated_data.get('role')
        email = validated_data.get('email')
        raw_username = validated_data['username']
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')

        prefix = ''
        if role == 'student':
            prefix = 'STU'
        elif role == 'teacher':
            prefix = 'TCH'
        elif role == 'moderator':
            prefix = 'MOD'

        user_count = User.objects.count()
        suffix = str(user_count + 1).zfill(4)

        final_username = f"{prefix}/{raw_username}/{suffix}"
        is_approved = True if role != 'moderator' else False

        if User.objects.filter(username=final_username).exists():
            raise serializers.ValidationError("User with this username already exists.")

        user = User.objects.create_user(
            username=final_username,
            email=email,
            password=validated_data['password'],
            role=role,
            is_approved=is_approved
        )

        # Save personal info
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        if role == 'student':
            Student.objects.get_or_create(
                user=user,
                defaults={
                    'name': raw_username,
                    'age': 0,
                    'student_id': final_username
                }
            )
        elif role == 'teacher':
            Teacher.objects.get_or_create(
                user=user,
                defaults={
                    'name': raw_username,
                    'age': 0,
                    'email': email,
                    'teacher_id': final_username
                }
            )

        if role == 'moderator':
            send_mail(
                subject="New Moderator Registration Request",
                message=f"A new moderator ({final_username}) has requested access. Please review and approve in the admin panel.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['admin@example.com'],
                fail_silently=True,
            )

        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['final_username'] = instance.username
        return rep

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        username = attrs.get('username', '')
        user = self.user

        if user.role == 'student' and not username.startswith('STU/'):
            raise serializers.ValidationError({'detail': 'Student must log in with STU/ prefix'})
        elif user.role == 'teacher' and not username.startswith('TCH/'):
            raise serializers.ValidationError({'detail': 'Teacher must log in with TCH/ prefix'})
        if user.role == 'moderator':
            if not username.startswith('MOD/'):
                raise serializers.ValidationError({'detail': 'Moderator must log in with MOD/ prefix'})
            if not user.is_approved:
                raise serializers.ValidationError({'detail': 'Moderator account is pending approval'})

        data['role'] = user.role
        data['username'] = user.username
        return data
