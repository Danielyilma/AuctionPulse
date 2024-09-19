from django.urls import path
from .views import NotificationListView, MarkAsReadView
from .consumer import NoticicationConsumer

urlpatterns = [
    path('list/', NotificationListView.as_view(), name='list-unread-notifications'),
    path('<int:pk>/update/', MarkAsReadView.as_view(), name='mark-as-read')
]

websocket_urlpatterns = [
    path('ws/bid/notification', NoticicationConsumer.as_asgi(), name='bid-notification')
]