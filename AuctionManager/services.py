from django.db import transaction
from django.utils import timezone
from rest_framework.serializers import ValidationError
from datetime import datetime
import pytz
from .tasks import start_auction, end_auction


@transaction.atomic
def update_auction(auction, bid_amount):
    '''atomic operation for auction current_bid update'''
    min_next_bid = (auction.bid_increment + float(auction.current_bid))
    start_price = float(auction.starting_price)

    if not (bid_amount >= start_price):
        raise ValidationError(f'Bid amount must be higher than starting price - {start_price}')
    
    if min_next_bid > bid_amount:
        raise ValidationError(f"Bid amount must be higher than the current bid. plus the bid increment - {min_next_bid}")
    
    auction.current_bid = bid_amount
    auction.save()


def schedule_auction_tasks(auction):
    '''schedule start and end time of auction'''
    start_delay = (auction.start_time - timezone.now()).total_seconds()
    end_delay = (auction.end_time - timezone.now()).total_seconds()

    start_auction.apply_async((auction.id,), countdown=start_delay)
    end_auction.apply_async((auction.id,), countdown=end_delay)


def adjust_timezone(timezone, datetime_str):
    '''convert user timezone to UTC timezone'''
    try:
        user_timezone = pytz.timezone(timezone)
        current_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    except pytz.UnknownTimeZoneError as e:
        raise ValidationError(e)
    except Exception as e:
        raise ValidationError(e)

    current_time = user_timezone.localize(current_time)
    target_utctime = current_time.astimezone(pytz.UTC)

    return target_utctime
