from django.shortcuts import render
from django.views import View
from store.models import *

from .forms import *


class CheckoutView(View):
    
    def get(self, request, *args, **kwargs):
        form=CheckoutForm()
        payment_method=PaymentmethodForm()
        order=Order.objects.get(user=request.user, ordered=False)

        context={
            'order':order,
            'form':form,
            'payment_method':payment_method
        }
        return render(request, 'payment/checkout.html', context)

    

        
