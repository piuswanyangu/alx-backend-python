from django.urls import path
from .views import UserListView, ConversationListView, MessageListView

urlpatterns = [
     path('users/', UserListView.as_view()),
     path('conversations/', ConversationListView.as_view()),
     path('messages/', MessageListView.as_view()),
]
