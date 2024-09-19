from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.serializers import ValidationError
from drf_spectacular.utils import extend_schema
from .serializers import AuctionSerializer, ImageSerializer, BidSerializer
from .models import Auction, Image
from .services import update_auction
from .tasks import push_bidinfo
from .doc_schema import auction_creation_schema
from notifications.tasks import notify_user_of_bid, bid_confirmation


@extend_schema(
    summary='Create auction',
    description='Endpoint to create an aution',
    request={
        "application/json": auction_creation_schema
    },
    responses=AuctionSerializer
)
class AuctionCreateView(generics.CreateAPIView):
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    summary="Get specific auction by id",
    description="Endpoint to get an auction",
    responses=AuctionSerializer
)
class AuctionGetView(generics.RetrieveAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [AllowAny]


@extend_schema(
    summary="Get Auctions",
    description='Endpoint to get auction listing for active auctions',
)
class AuctionListView(generics.ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [AllowAny]


@extend_schema(
    summary='Get images for an item',
    description='Endpoint to get the describing images for the item, required query param item_id',
    parameters=[
            {
                "name": "item_id",
                "in": "query",
                "description": "search image by the item_id",
                "required": True,
                "schema": {"type": "string"}
            }
    ]
)
class ImageRetrieveView(generics.ListAPIView):
    serializer_class = ImageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        item_id = self.request.query_params.get("item_id")
        return Image.objects.filter(item_id=item_id)


@extend_schema(
    summary='Bid Submission',
    description='Endpoint to submit a bid'
)
class BidSubmissionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BidSerializer

    def perform_create(self, serializer):
        auction = serializer.validated_data['auction']

        if not auction.is_active:
            raise ValidationError('Cannot place a bid on a closed or upcoming auction.')
        
        bidder = self.request.user

        if bidder == auction.seller:
            raise ValidationError('Seller Cannot place a bid on his auction item.')

        bid_amount = serializer.validated_data['amount']
        update_auction(auction, bid_amount)

        # Push bid information to the channel layer
        auction_serializer = AuctionSerializer(serializer.validated_data.get('auction'))
        push_bidinfo.delay(bidder.id, auction_serializer.data)
        notify_user_of_bid.delay(bidder.id, auction.id)
        bid_confirmation.delay(bidder.id, auction.id)

        serializer.save(bidder=bidder)
