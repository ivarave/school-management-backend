from .serializers import StudentSerializer
from rest_framework import viewsets
from .models import Student
from rest_framework.decorators import action
from rest_framework.response import Response

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=False, methods=['get'])
    def count(self, request):
        return Response({'count': Student.objects.count()})
    
