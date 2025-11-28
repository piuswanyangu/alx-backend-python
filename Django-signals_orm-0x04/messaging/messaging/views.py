from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from messaging_app.chats.models import Message

@login_required
def delete_user_account_view(request):
    """
    allows the current logged in user to delete their own account
    """
    if request.method == 'POST':
        user = request.user

        # log the user out immediately to prevent session issues
        logout(request)

        # this call triggers the post_delete signal before the record is removed from db
        user.delete()

        messages.success(request, "Your account and all related data have been successfully deleted")
        return redirect('home') 
    # for get request render a confirmation page
    return render(request, 'messaging/confirm_delete.html')

# view for displaying history
def message_history_view(request, pk):
    from .models import Message # type: ignore
    message = get_object_or_404(Message,pk=pk)
    history_records = message.history.all()
    context = {
        'message': message,
        'history_records': history_records,
    }
    return render(request, 'messaging/message_history.html', context)

def conversation_view(request):
    # fetch all root messages
    root_messages = Message.objects.filter(parent_message__isnull=True).order_by('timestamp').select_related(
        'sender',
        'receiver',
        'parent_message'
    ).prefetch_related(
        'replies',
        'replies__sender'
    )

    context = {
        'root_messages': root_messages,
    }

    return render(request, 'messaging/conversation.html',context)