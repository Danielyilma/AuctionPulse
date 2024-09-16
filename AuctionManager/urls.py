from django.urls import path
from .views import (
    AuctionCreateView, AuctionListView,
    AuctionGetView, ImageRetrieveView,
    BidSubmissionView
)
from .consumer import BidConsumer

urlpatterns = [
    path('auction', AuctionCreateView.as_view(), name='create-auction'),
    path('auction/list/', AuctionListView.as_view(), name='listing-auction'),
    path('auction/<int:pk>', AuctionGetView.as_view(), name='get-specific-auction'),

    path('image/', ImageRetrieveView.as_view(), name='get-item-image'),
    path('bid/', BidSubmissionView.as_view(), name='bid-submission'), 
]

websocket_urlpatterns = [
    path('ws/auction/<int:auction_id>', BidConsumer.as_asgi(), name="push-new-bidinfo")
]
