from django.db import models
import uuid
from base_model import TimeStampMixin

class Payment(TimeStampMixin, models.Model):
    auction = models.ForeignKey('AuctionManager.Auction', on_delete=models.CASCADE)
    user = models.ForeignKey('UserAccountManager.user', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10, 
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        default='pending'
    )
    currency = models.CharField(max_length=10, default='ETB')
    payment_id = models.CharField(max_length=255, unique=True)
    reason = models.CharField(max_length=60, default='auction_payment')

    @classmethod
    def create_payment(cls, auction, user, **kwargs):
        data = {
            'auction': auction,
            'user': user,
            'amount': auction.current_bid,
            'payment_id': str(uuid.uuid4()),
            **kwargs
        }

        return Payment.objects.create(**data)