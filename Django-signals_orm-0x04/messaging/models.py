from typing import Self
from django.db import models
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager
from messaging_app.chats.models import User

user = get_user_model()

class Message(models.Model):
    # foreign key to the user model for sender
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    # foreignkey to user model for the receiver
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # track if the message has been edited
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    # redefine the default manager objects
    objects = models.Manager()

    # add our custom manager ' unread'
    unread = UnreadMessagesManager() # type: ignore

    # self-referential ForeignKey
    # a message can optionally reply to another message
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies'
    )

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Message'
        verbose_name_plural = "Messages"
    

    def get_recursive_replies(self):
        """ recursive fetches all descendants """
        all_replies = list(self.replies.all())
        for reply in self.replies.all():
            all_replies.extend(reply.get_recursive_replies())
            return  all_replies

    def __str__(self):
        status = 'Read' if self.read else 'unread'
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')} ({'Reply' if self.parent_message else 'Root'}) ({status})"

class Notification(models.Model):
    # the user who is receiving the information
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    # the message that triggered this notification
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    # text to display for the notifications
    text = models.CharField(max_length=255)
    # status : has the user viewed the notification
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
    def __str__(self):
        return f"Notification for {self.user.username}: {self.text}"
    

# this model stores the old content every time a message is updated
class MessageHistory(models.Model):
    # link the message that ws edited
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    # THE CONTENT BEFORE THE CURRENT EDIT
    old_content = models.TextField()
    # the user who made the edits
    edited_by = models.ForeignKey(User, related_name='edited_history', on_delete=models.SET_NULL, null=True)
    # when edited happened
    edited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-edited_at']
        verbose_name = "Message History"

    def __str__(self):
        return f"History for Message {self.message.id} recorded at {self.edited_at.strftime('%Y-%m-%d %H:%M')}"
    
