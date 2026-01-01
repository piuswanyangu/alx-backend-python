from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserListView, ConversationListView, MessageListView

router = DefaultRouter()
router.register(r'messages', MessageListView, basename='message')

urlpatterns = [
     path('users/', UserListView.as_view()),
     path('conversations/', ConversationListView.as_view()),
     path('messages/', MessageListView.as_view()),
     # path('api', include(router.urls))
]
