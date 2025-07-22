from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'
    
    
class IsStudentReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.role == 'student' and
                request.method in SAFE_METHODS
        )
        
        
class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'moderator'