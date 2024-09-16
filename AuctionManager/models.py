from django.db import models
from base_model import TimeStampMixin
from datetime import timedelta
import os


class Auction(TimeStampMixin, models.Model):
    ''' Auction model'''
    title = models.CharField(max_length=60, blank=False)
    description = models.TextField()
    item = models.OneToOneField('Item', on_delete=models.CASCADE)
    seller = models.ForeignKey('UserAccountManager.User', on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(help_text='Duration in days')
    start_time = models.DateTimeField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=10,
        choices=[
            ('upcoming', 'Upcoming'),
            ('active', 'Active'),
            ('closed', 'Closed')
        ],
        default='upcoming'
    )

    @property
    def is_active(self):
        return self.status == 'active'

    @property
    def end_time(self):
        return self.start_time + timedelta(days=self.duration)
    
    @property
    def bid_increment(self):
        return float(self.current_bid) * 0.01

    def __str__(self) -> str:
        return f'Auction: {self.title} for {self.item.name}'
    

class Bid(TimeStampMixin, models.Model):
    ''' Bid model'''
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # max_amount = models.DecimalField(max_digits=10, decimal_places=2)
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE)
    bidder = models.ForeignKey('UserAccountManager.User', on_delete=models.CASCADE)


class Item(TimeStampMixin, models.Model):
    '''Item model'''
    name = models.CharField(max_length=60, blank=False)
    condition = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('used', 'Used'),
            ('refurbished', 'Refurbished'),
        ],
        default='new'
    )
    main_image = models.ImageField(upload_to='item_images/', blank=True)

    def delete(self, *args, **kwargs):
        if self.main_image and os.path.isfile(self.main_image.path):
            os.remove(self.main_image.path)
        
        super().delete(*args, **kwargs)


class Image(TimeStampMixin, models.Model):
    '''Image model'''
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='images')
    picture = models.ImageField(upload_to='item_images/', blank=True)

    def __str__(self) -> str:
        return f'{self.item.name}'
    
    def delete(self, *args, **kwargs):
        if self.picture and os.path.isfile(self.picture.path):
            os.remove(self.picture.path)
        
        super().delete(*args, **kwargs)
