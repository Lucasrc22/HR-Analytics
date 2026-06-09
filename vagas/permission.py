from rest_framework import permissions
class UserPermissionClass(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return request.user.has_perm('vagas.view_vaga')

        if request.method == 'POST':
            return request.user.has_perm('vagas.add_vaga')

        if request.method in ['PATCH', 'PUT']:
            return request.user.has_perm('vagas.change_vaga')

        if request.method == 'DELETE':
            return request.user.has_perm('vagas.delete_vaga')

        return False