from rest_framework import permissions

class GlobalDefaultPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # Obtém o nome da permissão baseado no método HTTP e no modelo
        model_permission_codename = self.__get_model_permission_codename(request.method, view)

        if not model_permission_codename:
            return False
        
        return request.user.has_perm(model_permission_codename)
    def __get_model_permission_codename(self, method, view):
        try:
            # Extrai informações do modelo através da view
            # view.queryset.model._meta fornece metadados do modelo (nome, app)
            model_name = view.queryset.model._meta.model_name  
            app_label = view.queryset.model._meta.app_label    

            # Converte o método HTTP para o suffix da permissão
            # GET → 'view', POST → 'add', etc
            action = self.__get_action_suffix(method)

            # Monta o codename final: "movies.view_movie"
            return f"{app_label}.{action}_{model_name}"

        except AttributeError:
            # Se a view não tiver queryset ou o modelo não existir, retorna None
            return None

    def __get_action_suffix(self, method):
        method_actions = {
            'GET': 'view',   
            'POST': 'add',      
            'PUT': 'change',    
            'PATCH': 'change',  
            'DELETE': 'delete', 
            'OPTIONS': 'view', 
            'HEAD': 'view',    
        }
        return method_actions.get(method, '')  # Retorna vazio se método não reconhecido