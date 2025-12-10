from django.urls import path, include
from rest_framework.routers import DefaultRouter

from messaging_app.chats import admin
from .views import UserListView, ConversationListView, MessageListView

router = DefaultRouter()
router.register(r'messages', MessageListView, basename='message')

urlpatterns = [
     # path('users/', UserListView.as_view()),
     # path('conversations/', ConversationListView.as_view()),
     # path('messages/', MessageListView.as_view()),
     # path('api', include(router.urls))
     path('admin/', admin.site.urls),
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'chats',
]
