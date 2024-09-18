from django.conf import settings
import requests
from UserAccountManager.serializers import UserSerializer
from .models import Payment

class ChapaPaymentService():
    '''Chapa payment service'''

    init_url = settings.CHAPA_INIT_URL
    transfer_init_url = settings.CHAPA_TRANSFER_INIT_URL
    secret_token = settings.CHAPA_SECRET_KEY
    callback_url = settings.APP_CALLBACK_URL_FORCHAPA
    verify_url = settings.CHAPA_VERIFIY_URL
    headers = {
        'Authorization': f"Bearer {secret_token}"
    }

    def get_paymenturl(self, auction, user):
        '''get payment url from chapa using chapa initialize url'''

        payment = Payment.create_payment(auction, user)
        user = UserSerializer(user).data

        payment_request = {
            'currency': 'ETB',
            'amount': payment.amount,
            'callback_url': self.callback_url,
            'tx_ref': payment.payment_id,
            **user 
        }

        response = requests.post(self.init_url, data=payment_request, headers=self.headers)

        if response.status_code != 200:
            raise ValueError('payment information not fullfiled')

        return response.json().get('data')['checkout_url']


    def verify_payment(self, payment, tx_ref):
        '''verify payment success'''

        verify_url = self.verify_url + tx_ref

        response = requests.get(verify_url, headers=self.headers)

        if response.status_code != 200:
            raise ValueError('payment information not fullfiled')

        payment_info = response.json()
        status = payment_info.get('status')

        payment.status = status
        payment.save()

        return {'message': payment_info.get('message'), 'status': payment_info.get('status')}


    def initiate_transfer(self, data, auction):
        '''initialize bank transfer to the user'''

        payment = Payment.create_payment(
            auction, auction.seller,
            reason='auction_seller_transfer',
            status='success'
        )
        data['amount'] = auction.current_bid
        data["currency"] = "ETB",
        data["reference"] = payment.payment_id

        response = requests.post(
            self.transfer_init_url,
            data=data,
            headers=self.headers
        )

        if response.status_code != 200:
            raise ValueError(response.json())

        return response.json()
