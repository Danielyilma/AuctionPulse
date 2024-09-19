from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .serializers import NotificationSerializer
from .models import Notification


@extend_schema(
    summary='List all unread notifications',
    description='list all unread notifications for a user',
    responses=NotificationSerializer
)
class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user, is_read=False)

@extend_schema(
    summary='mark as read',
    description='mark notification as read'

)
class MarkAsReadView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    http_method_names = ['patch']

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.mark_as_read()
