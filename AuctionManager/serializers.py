from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from .models import Item, Auction, Image, Bid
from .service import schedule_auction_tasks, adjust_timezone


class BidSerializer(serializers.ModelSerializer):
    '''serialize the bid model'''
    auction_id = serializers.PrimaryKeyRelatedField(queryset=Auction.objects.all(), source="auction")

    class Meta:
        model = Bid
        fields = ['amount', 'auction_id']


class ItemSerializer(serializers.ModelSerializer):
    '''serialize the Item model'''

    class Meta:
        model = Item
        fields = ["id", "name", "condition", "main_image"]


class ImageSerializer(serializers.ModelSerializer):
    '''serialize the Image model'''

    class Meta:
        model = Image
        fields = ["picture"]

@extend_schema_serializer(exclude_fields=['images', 'timezone'])
class AuctionSerializer(serializers.ModelSerializer):
    '''
        - serialize the Auction with auction item and the item's images model
        - set the attribute start_time to UTC timezone with respect to user timezone
        - schedule the auction start and end time after the object is created
    '''
    item = ItemSerializer()
    images = ImageSerializer(many=True, read_only=True)
    timezone = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Auction
        exclude = ['seller', 'status']
    
    def create(self, validated_data):
        request = self.context['request']
        seller = request.user

        item_data = validated_data.pop('item')
        item = Item.objects.create(**item_data)

        user_timezone = request.data.get('timezone')
        start_time = request.data.get('start_time')

        validated_data['start_time'] = adjust_timezone(user_timezone, start_time)

        images = request.FILES.getlist('images')
        for image in images:
            image_data = {'picture': image}
            Image.objects.create(item=item, **image_data) 

        validated_data['item'] = item
        validated_data['seller'] = seller
        validated_data['status'] = 'upcoming'
        auction = Auction.objects.create(**validated_data)
        schedule_auction_tasks(auction)
        return auction
