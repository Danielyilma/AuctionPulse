from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.serializers import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from AuctionManager.models import Auction
from notifications.tasks import payment_notification
from .models import Payment
from .services import ChapaPaymentService
from .serializers import VerifySerializer, TransferSerializer


@extend_schema(
    summary='winner payment route',
    description='Returns Process payment url for the auction winner.',
    responses={
        200: OpenApiResponse(
            response=dict,
                description='Returns the payment URL for the user to proceed with the payment.',
                examples=[
                    OpenApiExample(
                        'Example Response',
                        value={"payment_url": "http://example.com"}
                    )
                ]
        ),
        404:  OpenApiResponse(
            description='Auction not found'
        ),
    }
)
class ChapaPaymentRedirectView(APIView):
    '''Chapa payment initialization redirect url'''
    permission_classes = [IsAuthenticated]

    def get(self, request, auction_id):
        auction = Auction.objects.get(id=auction_id)

        chapa = ChapaPaymentService()
        payment_url = chapa.get_paymenturl(auction, request.user)

        return Response({'payment_url': payment_url}, status=status.HTTP_302_FOUND)


@extend_schema(
    summary='Tranfer Payment',
    request=TransferSerializer,
    responses=VerifySerializer
)
class ChapaTransferInitView(APIView):
    '''chapa bank transfer initialization'''
    permission_classes = [IsAuthenticated]

    def post(self, request, auction_id):
        auction = Auction.objects.get(id=auction_id)
        user = request.user

        if user != auction.seller:
            return Response(
                {'error': f'Wrong owner of the auction item {auction.title} - {auction.id}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
        if auction.status != 'closed':
            return Response({'error': 'The auction is not yet closed'}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.filter(auction=auction, reason='auction_payment').first()

        if not payment and payment.status != 'success':
            return Response({'error': 'The winning bidder has not yet paid'}, status=status.HTTP_400_BAD_REQUEST)
        
        payment = Payment.objects.filter(auction=auction, user=user).first()

        if payment and payment.status == 'success':
            return Response(
                {'error': f'the payment has already been made status - {payment.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        chapa = ChapaPaymentService()

        try:
            serializer = TransferSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            payment_data = chapa.initiate_transfer(serializer.validated_data, auction)
        except (ValueError, ValidationError) as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(payment_data, status=status.HTTP_200_OK)


@extend_schema(
    summary='Verify Payment',
    responses=VerifySerializer
)
class ChapaPaymentVerifyView(APIView):
    '''Chapa's accept payment verification'''
    permission_classes = [AllowAny]

    def get(self, request):
        tx_ref = request.query_params.get('trx_ref')
        payment = Payment.objects.filter(payment_id=tx_ref).first()

        if not Payment:
            return Response({'error': "CSRF check fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        chapa = ChapaPaymentService()
        payment_info = chapa.verify_payment(payment, tx_ref)

        if payment_info['status'] == 'success':
            message = 'We are pleased to confirm that we have received your payment'
        else:
            message = 'Your payment failed'
        
        payment_notification(message, payment.id)

        return Response(payment_info, status=status.HTTP_200_OK)
