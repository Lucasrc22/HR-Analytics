from rest_framework import permissions

class UserPermissionClass(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'OPTIONS', 'HEAD']:
            return request.user.has_perm('cat.view_cat')

        if request.method == 'POST':
            return request.user.has_perm('cat.add_cat')

        if request.method in ['PATCH', 'PUT']:
            return request.user.has_perm('cat.change_cat')

        if request.method == 'DELETE':
            return request.user.has_perm('cat.delete_cat')

        return False