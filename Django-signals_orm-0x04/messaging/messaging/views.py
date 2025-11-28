from django.shortcuts import render, get_object_or_404
from .models import Message # pyright: ignore[reportMissingImports]

def message_history_view(request, pk):
    """
    Displays the current message and all its previous versions.
    """
    # 1. Fetch the primary message object, or return a 404 if it doesn't exist
    message = get_object_or_404(Message, pk=pk)
    
    # 2. Fetch the history records related to this message.
    # The 'history' is the related_name we defined in the MessageHistory model.
    # We order by edited_at descending to show the most recent changes first.
    history_records = message.history.all()
    
    # 3. Create the context dictionary to pass data to the template
    context = {
        'message': message,
        'history_records': history_records,
    }
    
    # 4. Render the template
    return render(request, 'messaging/message_history.html', context)