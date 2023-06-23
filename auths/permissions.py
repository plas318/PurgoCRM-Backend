from rest_framework.permissions import BasePermission

class isAdmin(BasePermission):
    '''
    IsAdmin permission - Checks if user is admin
    '''
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin

class isOwner(BasePermission):
    '''
    IsOwner Permission - Checks if user is owner
    '''
    def has_object_permission(self, request, view, obj):
        
        return obj == request.user

class isManager(BasePermission):
    '''
    IsManager Permission - Checks if user is Manager of the hospital
    '''
    def has_object_permission(self, request, view, obj):
        
        return obj.manager == request.user

        