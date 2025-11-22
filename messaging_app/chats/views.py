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


class ConversationListView(generics.ListCreateAPIView):
    permission_classes = [ permissions.IsAuthenticated, IsParticipantOfConversation]
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


class MessageListView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
