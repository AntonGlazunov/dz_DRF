from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsModer(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moder').exists()


class IsAuthenticatedAndNoModer(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and not request.user.groups.filter(name='Moder').exists():
            return True
