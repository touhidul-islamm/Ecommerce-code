from django.urls import path
from . views import *

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('sslc_status/',sslc_status, name='status'),
    path('sslc_complete/<val_id>/<tran_id>/',sslc_complete, name='sslc_complete'),
]