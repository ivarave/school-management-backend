from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('moderator', 'Moderator'),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-/]+$',
                message="Username may contain letters, digits, and @/./+/-/_ and / characters."
            )
        ]
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_approved = models.BooleanField(default=True) 
    

class Student(models.Model):
    name = models.CharField(max_length=100, default ='')
    age = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50)
    email = models.EmailField(default='')
    
    
    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    name = models.CharField(max_length=100, default ='')
    age = models.PositiveIntegerField(default=0)
    email = models.EmailField(default='')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username

class Subject(models.Model):
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey('ClassRoom', on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class ClassRoom(models.Model):
    name = models.CharField(max_length=50)
    students = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return self.name

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name}"

class Timetable(models.Model):
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    time = models.TimeField()

    def __str__(self):
        return f"{self.class_room.name} - {self.subject.name} ({self.day})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[("Present", "Present"), ("Absent", "Absent")])

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"

class classAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[("Present", "Present"), ("Absent", "Absent")])

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"
