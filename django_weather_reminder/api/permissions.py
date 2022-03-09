from rest_framework.permissions import BasePermission


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsUserSubscription(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
