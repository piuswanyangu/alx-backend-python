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
            # allow only authenticated users to access api
        return request.user and request.user.is_authenticated
            
        
        
    def has_object_permission(self, request, view, obj):
            # allow only participants of conversation to access object
        if hasattr(obj,'participants'):
                # determines the conversation
            conversation = obj
            # When accessing a Message object (e.g., PUT /messages/1/):
            # We need to access the related conversation through the message object.
        elif hasattr(obj,'conversation'):
                conversation = obj.conversation
            
            # deny access if object structure is unexpected
        else:
            return False
            
        is_participant = request.user in conversation.participants.all()
        return is_participant