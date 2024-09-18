from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    # schema and docs endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # User management endpoints
    path('api/user/', include('UserAccountManager.urls'), name='auth-token'),

    # Auction management endpoints
    path('api/', include('AuctionManager.urls'), name='auction-managment'),

    path('api/payment/', include('Payments.urls'), name='payment-redirect')
]
