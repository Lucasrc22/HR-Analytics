from rest_framework import permissions

class UserPermissionClass(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return request.user.has_perm('legal_persons.view_legal_person')

        if request.method == 'POST':
            return request.user.has_perm('legal_persons.add_legal_person')

        if request.method in ['PATCH', 'PUT']:
            return request.user.has_perm('legal_persons.change_legal_person')

        if request.method == 'DELETE':
            return request.user.has_perm('legal_persons.delete_legal_person')

        return False