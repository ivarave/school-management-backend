from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTeacherOrModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in SAFE_METHODS:
            return True

        if user.role == "moderator":
            return True

        if user.role == "teacher":
            return obj.teacher == user

        return False
