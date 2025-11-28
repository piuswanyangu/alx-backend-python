from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

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

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    signal handler that runs Before a message object is saved
    it checks if the message is an update
    """
    # check if the instance already exists in the database
    # This  prevents running on the initial creation
    if instance.pk:
        try:
            # retrieve the old version of object from database
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return
        # compare the old content with the new  content
        if old_message.content != instance.content:
            # create the history record with the old content
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content,
                edited_by=instance.sender


            )
            # Mark the instance as dited before it is saved
            instance.edited = True
            #  The new content (instance.content) is saved by the default Message.save() 
            # after this signal handler finishes.