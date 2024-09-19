from django.db import models

class Notification(models.Model):
    user = models.ForeignKey('UserAccountManager.User', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=60, choices=[
        ('bid', 'Bid Notification'),
        ('auction_end', 'Auction End Notification'),
        ('outbid', 'Outbid Notification'),
        ('payment', 'Payment Notification')
    ])

    def __str__(self):
        return f'Notification for {self.user.email}: {self.notification_type}'

    def mark_as_read(self):
        self.is_read = True
        self.save()