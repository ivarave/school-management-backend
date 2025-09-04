from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTeacherOrModerator(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == "student" and request.method not in SAFE_METHODS:
            return False
        return True