from rest_framework import viewsets
from .models import Grade
from .serializers import GradeSerializer
from .permissions import IsTeacherOrModerator

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsTeacherOrModerator]

    def get_queryset(self):
        user = self.request.user
        if user.role == "student":
            return Grade.objects.filter(student__user=user)
        elif user.role in ["teacher", "moderator"]:
            return Grade.objects.all()
        return Grade.objects.none()
