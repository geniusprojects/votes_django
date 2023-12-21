from rest_framework.permissions import BasePermission


class GetIfAuthor(BasePermission):
    """
    Allows access only to "author group" users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Author').exists()


class PostIfAuthor(BasePermission):
    """
    Allows access only to "author group" users.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.groups.filter(name='Author').exists()
        else:
            return True
