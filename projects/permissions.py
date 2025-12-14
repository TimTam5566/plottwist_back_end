'''
permissions.py is the access comtrol module for the project. 
It defines custom permission classes
to manage user access based on ownership and support roles.
'''

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    ============================================================
    CUSTOM PERMISSION: Only owners can modify their projects
    ============================================================
    
    WHAT IT DOES:
    - Anyone can READ (GET) a project
    - Only the OWNER can EDIT (PUT) or DELETE a project
    
    USED ON: ProjectDetail view
    
    EXAMPLE:
    - Sarah creates "Haunted Lighthouse" (she's the owner)
    - Tim can VIEW the project 
    - Tim CANNOT edit the project 
    - Sarah CAN edit her own project 
    """
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS') - read-only methods
        if request.method in permissions.SAFE_METHODS:
            return True # Anyone can read
        # For write methods (PUT, PATCH, DELETE), check ownership
        return obj.owner == request.user
        # obj = the project being accessed
        # request.user = the logged-in user
        # Returns True only if they match

class IsSupporterOrReadOnly(permissions.BasePermission):
    """
    ============================================================
    CUSTOM PERMISSION: Only pledge creators can modify their pledges
    ============================================================
    
    WHAT IT DOES:
    - Anyone can READ (GET) a pledge
    - Only the SUPPORTER (person who made it) can EDIT or DELETE
    
    USED ON: PledgeDetail view
    
    EXAMPLE:
    - Tim contributes to "Haunted Lighthouse" (he's the supporter)
    - Sarah can VIEW Tim's contribution 
    - Sarah CANNOT edit Tim's contribution 
    - Tim CAN edit his own contribution 
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True # Anyone can read
        return obj.supporter == request.user
        # obj.supporter = who made this pledge