from celery import shared_task
from .models import Auction
from django.utils import timezone

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
        auction.save()
