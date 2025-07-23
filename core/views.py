# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsTeacher, IsStudentReadOnly, IsModerator
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializers import (RegisterSerializer,CustomTokenObtainPairSerializer,StudentSerializer, TeacherSerializer,SubjectSerializer, GradeSerializer, ClassRoomSerializer, TimetableSerializer, AttendanceSerializer,  ClassAttendanceSerializer,  CustomUserSerializer, TeacherInfoSerializer)
from .models import Student, Teacher, Subject, Grade, ClassRoom, Timetable, Attendance, classAttendance, CustomUser

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_info(request):
    user = request.user
    if user.role != 'student' or 'moderator':
        return Response({'error': 'Not authorized'}, status=403)
    try:
        student = Student.objects.get(user=request.user)
        return Response({
            'id': student.id,
            'name': student.name,
            'age': student.age,
            'student_id': student.student_id,
            'email': request.user.email,
            'username': request.user.username,
            'role': request.user.role,
        })
    except Student.DoesNotExist:
        return Response({'error': 'Student profile not found'}, status=404)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_info(request):
    user = request.user
    if user.role != 'teacher' or 'moderator':
        return Response({'error': 'Not authorized'}, status=403)

    try:
        teacher = Teacher.objects.get(user=user)
        data = {
            "username": teacher.user.username,
            "email": teacher.user.email,
            "teacher_id": teacher.teacher_id,
        }
        return Response(data)
    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found"}, status=404)



class UserManagementViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsModerator]

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "message": "Registration successful",
            "final_username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role
        }, status=status.HTTP_201_CREATED)
        
                
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(role='student')
    serializer_class = StudentSerializer
    permission_classes = [IsTeacher | IsStudentReadOnly | IsModerator |IsAuthenticated]




class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsTeacher | IsStudentReadOnly | IsModerator|IsAuthenticated]
    
class ModeratorViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsModerator|IsAuthenticated]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsTeacher | IsStudentReadOnly | IsModerator|IsAuthenticated]


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsTeacher | IsStudentReadOnly | IsModerator|IsAuthenticated]


class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    permission_classes = [IsTeacher | IsStudentReadOnly | IsModerator|IsAuthenticated]


class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [IsTeacher | IsStudentReadOnly | IsModerator|IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsTeacher | IsStudentReadOnly | IsModerator|IsAuthenticated]


class ClassAttendanceViewSet(viewsets.ModelViewSet):
    queryset = classAttendance.objects.all()
    serializer_class = ClassAttendanceSerializer
    permission_classes = [IsTeacher | IsStudentReadOnly | IsModerator|IsAuthenticated]
