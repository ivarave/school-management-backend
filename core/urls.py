from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from .views import (RegisterView, CustomTokenObtainPairView, StudentViewSet, TeacherViewSet, SubjectViewSet, GradeViewSet, ClassRoomViewSet, TimetableViewSet, AttendanceViewSet, ClassAttendanceViewSet, ChangePasswordView, ModeratorViewSet, UserManagementViewSet, student_info, teacher_info)

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'classrooms', ClassRoomViewSet)
router.register(r'timetable', TimetableViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'classattendance', ClassAttendanceViewSet)
router.register(r'mod/users', ModeratorViewSet,basename='mod-users')
router.register(r'manage-users', UserManagementViewSet, basename='manage-users')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('student-info/', student_info, name='student-info'),
    path('teacher-info/', teacher_info, name='teacher-info'),
    path('', include(router.urls)),
]
