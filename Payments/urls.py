from django.urls import path
from .views import ChapaPaymentRedirectView, ChapaPaymentVerifyView, ChapaTransferInitView

urlpatterns = [
    path('redirect/<int:auction_id>', ChapaPaymentRedirectView.as_view(), name='chapa_redirect'),
    path('verify', ChapaPaymentVerifyView.as_view(), name='payment-verification'),
    path('transfer/<int:auction_id>', ChapaTransferInitView.as_view(), name='seller-payment')
]
