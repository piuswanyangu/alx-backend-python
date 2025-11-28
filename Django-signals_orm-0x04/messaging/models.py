from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()

class Message(models.Model):
    # foreign key to the user model for sender
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    # foreignkey to user model for the receiver
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Message'
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class Notification(models.Model):
    # the user who is receiving the information
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    # the message that triggerred this notification
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
    
