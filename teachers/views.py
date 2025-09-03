from rest_framework import viewsets
from .models import Teacher 
from .serializers import TeacherSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [AllowAny]


    @action(detail=False, methods=['get'])
    def count(self, request):
        count = Teacher.objects.count()
        return Response({'count': count})