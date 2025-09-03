# subjects/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Subject
from teachers.models import Teacher
from .serializers import SubjectSerializer
from server.permissions import IsTeacherOrModeratorOrReadOnly
from rest_framework import status
from rest_framework.exceptions import NotFound


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrModeratorOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user

        if user.role == "moderator":
            return Subject.objects.all()
        elif user.role == "teacher":
            try:
                teacher = Teacher.objects.get(user=user)
            except Teacher.DoesNotExist:
                raise NotFound("Teacher profile not found for this user")
            return Subject.objects.filter(teacher=teacher)
        elif user.role == "student":
            return Subject.objects.filter(students=user)
        return Subject.objects.none()

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def count(self, request):
        return Response({"count": Subject.objects.count()})

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == "teacher":
            try:
                teacher = Teacher.objects.get(user=user)
            except Teacher.DoesNotExist:
                raise NotFound("Teacher profile not found for this user")
            serializer.save(teacher=teacher)

        elif user.role == "moderator":
            serializer.save()

        else:
            return PermissionDenied("You do not have permission to create a subject.")

    def perform_update(self, serializer):
        user = self.request.user
        subject = self.get_object()

        if user.role == "moderator":
            serializer.save()
        elif user.role == "teacher":
            try:
                teacher = Teacher.objects.get(user=user)
            except Teacher.DoesNotExist:
                raise NotFound("Teacher profile not found for this user")
            if subject.teacher == teacher:
                serializer.save()
            else:
                raise PermissionDenied("You do not have permission to edit this subject.")
        else:
            raise PermissionDenied("You do not have permission to edit this subject.")




    def perform_destroy(self, instance):
        user = self.request.user

        if user.role == "moderator" or (
            user.role == "teacher" and instance.teacher == user
        ):
            instance.delete()

        else:
            raise PermissionDenied("You do not have permission to delete this subject.")

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        subject = self.get_object()
        user = request.user

        if user.role != "student":
            raise PermissionDenied("Only students can enroll in subjects.")

        subject.students.add(user)
        return Response(
            {"status": f"{user.username} enrolled in {subject.name}"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def unenroll(self, request, pk=None):
        subject = self.get_object()
        user = request.user

        if user.role != "student":
            raise PermissionDenied("Only students can unenroll from subjects.")

        subject.students.remove(user)
        return Response(
            {"status": f"{user.username} unenrolled from {subject.name}"},
            status=status.HTTP_200_OK,
        )