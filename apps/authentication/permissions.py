# apps/authentication/permissions.py (o donde quieras guardarlo)
from rest_framework import permissions
from .models import User
from .models import AuthGroup


class IsSpecificGroup(permissions.BasePermission):
    allowed_groups = []
    message = "No tienes permiso para acceder."

    def has_permission(self, request, view):
        # Obtener el usuario de tu modelo User
        try:
            user = User.objects.get(username=request.user.username)
            # Obtener el grupo basado en el ID almacenado en user.role
            user_group = AuthGroup.objects.get(id=user.role)
            # Verificar si el nombre del grupo está en la lista permitida
            return user_group.name in self.allowed_groups
        except (User.DoesNotExist, AuthGroup.DoesNotExist):
            return False
