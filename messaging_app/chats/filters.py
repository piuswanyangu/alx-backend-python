import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # filter by specifi user
    user = django_filters.NumberFilter(method='filter_by_user')
    # filter by sender
    sender = django_filters.NumberFilter(field_name='sender__id')
    # filter by recipient
    recipient = django_filters.NumberFilter(field_name='recipient__id')
    # filter by date range
    timestamp_after = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='gte',
        label='Message after'
    )
    timestamp_before = django_filters.DateTimeFilter(
        field_name='timestamp',
        lookup_expr='lte',
        label='Messages before'
    )
    # filter by read status
    is_read = django_filters.BooleanFilter(field_name='is_read')
    # search in content
    content = django_filters.CharFilter(
        field_name='content',
        lookup_expr='icontains',
        label='Search in content'
    )

class Meta:
    model =  Message
    fields = [ 'sender', 'recipient', 'is_read', 'content']

def filter_by_ser(self, queryset, name, value):
    # filter messages where user is either sender or receiver
    return queryset.filter(
        models.Q(sender__id=value) | models.Q(recipient__id=value)
    )   