from rest_framework import viewsets
from .models import Moderator 
from .serializers import ModeratorSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class ModeratorViewSet(viewsets.ModelViewSet):
    queryset = Moderator.objects.all()
    serializer_class = ModeratorSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = Moderator.objects.count()
        return Response({'count': count})
    
