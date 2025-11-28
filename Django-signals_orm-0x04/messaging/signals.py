from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

# the @receiver decorator connects the function below to the post_save signals
# of he message model
@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created,**kwargs):
    """
    signal handler that creates a Notification object
    for the message's receiver when a new Message is saved
    """
    # created is a boolean flag that is True if a new record was inserted
    if created:
        # get the receiver user from the newly created Message  instance
        receiver_user = instance.receiver
        sender_username = instance.sender.username

        # construct the notification text
        notification_text = f"New Message from {sender_username}"

        # create the notification instance
        Notification.objects.create(
            user=receiver_user,
            message=instance,
            text=notification_text
        )