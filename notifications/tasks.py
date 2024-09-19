from celery import shared_task
from AuctionManager.models import Auction
from UserAccountManager.models import User
from Payments.models import Payment
from .services import send_notifications

@shared_task
def notify_user_of_bid(current_bidder, auction_id):
    '''notify all bidder when their is a new bid on the auction follow'''

    auction = Auction.objects.get(id=auction_id)
    message = f"A new bid of {auction.current_bid} has been placed on the auction '{auction.title}'"

    users_with_bids = User.objects.filter(
        bid__auction_id=auction_id
    ).exclude(id=current_bidder).distinct()

    users_with_bids = list(users_with_bids) + [auction.seller]
    send_notifications(message, users_with_bids, 'bid')


@shared_task
def bid_confirmation(bidder_id, auction_id):
    '''confirms bidder when the bid is successfull'''

    auction = Auction.objects.get(id=auction_id)
    message = f'''Thank you for participating in our auction! We are \
        pleased to confirm that your bid of {auction.current_bid} has been \
        successfully placed for the item '{auction.title}''.'''
    
    users = User.objects.filter(id=bidder_id)
    send_notifications(message, users, 'bid')


@shared_task
def notify_auction_close(auction_id):
    '''notify the seller when the auction is closed'''

    auction = Auction.objects.get(id=auction_id)
    message = f'''We would like to inform you that the auction 
    for "{auction.title}" has now officially closed.'''

    users_with_bids = User.objects.filter(
        bid__auction_id=auction_id
    ).distinct()

    users_with_bids = list(users_with_bids) + [auction.seller]
    send_notifications(message, users_with_bids, 'auction_end')


@shared_task
def payment_notification(message, payment_id):
    '''notify the status of a payment'''

    payment = Payment.objects.get(id=payment_id)
    auction = payment.auction
    user = payment.user

    message_detail = f''' for the auction item {auction.title}.
        Payment Details:
        Transaction ID: {payment.payment_id}
        Amount: {payment.amount} {payment.currency}
        Payment Date: {payment.updated_at}
        Item: {auction.title}
        status: {payment.status}
        Winning Bidder email: [{user.first_name} ({user.email})
'''
    
    message += message_detail
    send_notifications(message, [user], 'payment')