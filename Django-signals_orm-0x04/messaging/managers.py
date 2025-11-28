# messaging/managers.py

from django.db import models
from django.db.models import QuerySet

class UnreadMessagesQuerySet(QuerySet):
    """Custom QuerySet methods for unread messages."""
    
    def by_user(self, user):
        """Filters messages received by the user that are unread."""
        # This contains the core filtering logic
        return self.filter(receiver=user, read=False)

class UnreadMessagesManager(models.Manager):
    """Custom manager that uses the specialized QuerySet."""
    
    def get_queryset(self):
        # Ensures all lookups through this manager use our custom QuerySet class
        return UnreadMessagesQuerySet(self.model, using=self._db)

    def unread_for_user(self, user):
        """Public method to fetch unread messages for a given user."""
        return self.get_queryset().by_user(user)