
from rest_framework import generics, filters
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
# import custom permissions 
from .permissions import IsOwnerOfObject
from .permissions import IsParticipantOfConversation
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
# NEW IMPORTS
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter
from .pagination import MessagePagination


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# --- Conversation Views ---
class ConversationListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    serializer_class = ConversationSerializer
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).distinct()


class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


# --- Message Views ---
class MessageListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    serializer_class = MessageSerializer
    
    # NEW: Add pagination
    pagination_class = MessagePagination
    
    # NEW: Add filter backends
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = MessageFilter
    
    # NEW: Add ordering options
    ordering_fields = ['timestamp', 'sender']
    ordering = ['-timestamp']  # Default ordering: newest first
    
    # NEW: Add search fields
    search_fields = ['message_body', 'sender__username']

    def get_queryset(self):
        # Get IDs of conversations the user is a participant of
        user_conversation_ids = Conversation.objects.filter(
            participants=self.request.user
        ).values_list('id', flat=True)
        
        # Filter messages belonging to those conversations
        return Message.objects.filter(
            conversation_id__in=user_conversation_ids
        ).select_related('sender', 'conversation')  # Optimization

    def perform_create(self, serializer):
        # Retrieve 'conversation_id' from request data.
        conversation_id = self.request.data.get('conversation') 
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        
        # Check if the user is a participant before saving.
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer