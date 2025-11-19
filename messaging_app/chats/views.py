from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Conversation, Message
from.serializers import (UserSerializer,ConversationSerializer,MessageSerializer)


# User Registration
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# create & list conversations
class CreateConversationView(APIView):
    def post(self, request):
        participant_ids = request.data.get("participants",[])

        if len(participant_ids) == 0:
            return Response({"error":"Provide at least one participant ID"}, status=400)
        
        Conversation = Conversation.objects.create()
        Conversation.participants.set(participant_ids)
        Conversation.save()

        serializer = ConversationSerializer(Conversation)
        return Response(serializer.data, status=201)
