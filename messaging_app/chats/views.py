from rest_framework import generics
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
# import custom permissions 
from .permissions import IsOwnerOfObject
from .permissions import IsParticipantOfConversation
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# --- Conversation Views ---
class ConversationListView(generics.ListCreateAPIView):
    permission_classes = [ permissions.IsAuthenticated, IsParticipantOfConversation]
    # queryset = Conversation.objects.all() # The queryset should be filtered in get_queryset
    serializer_class = ConversationSerializer
    
    # [Addition]: Filters the list view to only show conversations the user is a participant of.
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).distinct()

# [Addition]: Handles retrieval, update, and deletion of a single conversation.
class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ permissions.IsAuthenticated, IsParticipantOfConversation]
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


# --- Message Views ---
class MessageListView(generics.ListCreateAPIView):
    # [Addition]: Applies the necessary permissions.
    permission_classes = [ permissions.IsAuthenticated, IsParticipantOfConversation]
    # queryset = Message.objects.all() # The queryset should be filtered in get_queryset
    serializer_class = MessageSerializer

    # [Addition]: Filters the list view to only show messages within the user's conversations.
    def get_queryset(self):
        # Get IDs of conversations the user is a participant of
        user_conversation_ids = Conversation.objects.filter(participants=self.request.user).values_list('id', flat=True)
        # Filter messages belonging to those conversations
        return Message.objects.filter(conversation_id__in=user_conversation_ids)

    # [Addition]: Custom creation logic to check participation and set sender/conversation.
    def perform_create(self, serializer):
        # Retrieve 'conversation_id' from request data.
        conversation_id = self.request.data.get('conversation') 
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        
        # Check if the user is a participant before saving.
        if self.request.user not in conversation.participants.all():
            # Triggers a HTTP 403 Forbidden response.
            raise PermissionDenied("You are not a participant of this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)

# [Addition]: Handles retrieval, update, and deletion of a single message.
class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ permissions.IsAuthenticated, IsParticipantOfConversation]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer