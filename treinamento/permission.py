from rest_framework import permissions

class UserPermissionClass(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return request.user.has_perm('treinamento.view_treinamento')

        if request.method == 'POST':
            return request.user.has_perm('treinamento.add_treinamento')

        if request.method in ['PATCH', 'PUT']:
            return request.user.has_perm('treinamento.change_treinamento')

        if request.method == 'DELETE':
            return request.user.has_perm('treinamento.delete_treinamento')

        return False