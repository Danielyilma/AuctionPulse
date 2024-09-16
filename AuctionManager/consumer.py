from channels.generic.websocket import AsyncWebsocketConsumer

class BidConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.auction_group_name = f'auction_{self.auction_id}'

        await self.channel_layer.group_add(
            self.auction_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.auction_group_name,
            self.channel_name
        )

    async def new_bid(self, event):
        bid = event['bid']

        await self.send(text_data=bid)
