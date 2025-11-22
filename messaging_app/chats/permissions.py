from rest_framework import permissions
class IsOwnerOfObject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # write permissions are only allowed to owner of the object
        return obj.owner == request.user
    
    class IsParticipantOfConversation(permissions.BasePermission):
        # permissions to only allow participants of conversation to 
        # view, send, update and delete message within it
        def has_permission(self, request, view):
            # allow only authenticated users to acces api
            if request.user and request.user.is_authenticated:
                return True
            return False
        
        def has_object_permission(self, request, view, obj):
            # allow only participants of conversation to access object
            if hasattr(obj,'participants'):
                # the obj is the convesation instances
                return request.user in obj.participants.all()
            # When accessing a Message object (e.g., PUT /messages/1/):
            # We need to access the related conversation through the message object.
            elif hasattr(obj,'conversation'):
                return request.user in obj.conversation.participants.all()
            
            # deny access if object structure is unexpected
            return False