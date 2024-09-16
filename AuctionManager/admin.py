from django.contrib import admin
from .models import Auction, Bid, Image, Item

admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Image)
admin.site.register(Item)