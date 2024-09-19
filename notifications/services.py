from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from.serializers import NotificationSerializer

def send_notifications(message, users, bid_type):
    ''' sends notification message for users'''
    for user in users:
        notification = Notification.objects.create(
            user=user,
            notification_type=bid_type,
            message=message
        )
        serializer = NotificationSerializer(notification)

        channel_layer = get_channel_layer()
        group_name = f'user_{user.id}'


        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification',
                'message': serializer.data
            }
        )