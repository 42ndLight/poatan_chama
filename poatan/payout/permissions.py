from rest_framework import permissions

class IsChamaAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'chama'):
            return obj.chama.admin == request.user        

        chama_id = request.data.get('chama_id') or view.kwargs.get('chama_id')
        if chama_id:
            from cashpool.models import Chama
            chama = Chama.objects.get(pk=chama_id)
            return chama.admin == request.user
        
        return False