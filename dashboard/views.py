from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from students.models import Student
from teachers.models import Teacher
from moderators.models import Moderator
from users.models import CustomUser

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):

    students_count = CustomUser.objects.filter(role=CustomUser.STUDENT).count()
    teachers_count = CustomUser.objects.filter(role=CustomUser.TEACHER).count()
    moderator_count = CustomUser.objects.filter(role=CustomUser.MODERATOR).count()

    male_count = CustomUser.objects.filter(gender='male').count()
    female_count = CustomUser.objects.filter(gender='female').count()
    other_count = CustomUser.objects.filter(gender='other').count()

    return Response({
        "students": students_count,
        "teachers": teachers_count,
        "moderators": moderator_count,
        "gender_ratio": {
            "male": male_count,
            "female": female_count,
            "other": other_count,
        }
    })
