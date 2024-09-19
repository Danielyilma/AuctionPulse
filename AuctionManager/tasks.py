from celery import shared_task
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from notifications.tasks import notify_auction_close
from .models import Auction


@shared_task
def start_auction(auction_id):
    '''celery task to change auction status to active'''
    auction = Auction.objects.get(id=auction_id)
    if auction.start_time <= timezone.now():
        auction.status = 'active'
        auction.save()


@shared_task
def end_auction(auction_id):
    '''celery task to change auction status to closed'''
    auction = Auction.objects.get(id=auction_id)
    if auction.end_time <= timezone.now():
        auction.status = 'closed'
        notify_auction_close(auction_id)
        auction.save()


@shared_task
def push_bidinfo(bidder_id, data):
    '''update the auction information in realtime'''

    bid_info = {
        'bidder': bidder_id,
        'auction': data,
        'amount': float(data.get('current_bid'))
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'auction_{bid_info["auction"]["id"]}',
        {
            'type': 'new_bid',
            'bid': json.dumps(bid_info)
        }
    )