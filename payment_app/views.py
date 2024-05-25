from django.shortcuts import redirect, render
from django.views import View
from store.models import *
from .forms import *

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse

import json
from django.conf import settings
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

class CheckoutView(View):
    
    def get(self, request, *args, **kwargs):
        form = CheckoutForm()
        order=Order.objects.get(user=request.user, ordered=False)
        payment_method = PaymentMethodForm()
        context={
            'order':order,
            'form':form,
            'payment_method':payment_method,
            }
        return render(request, 'payment/checkout.html', context)

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST)
        payment_obj=Order.objects.filter(user=request.user, ordered=False)[0]
        payment_form=PaymentMethodForm(instance=payment_obj)

        if request.method=='post' or request.method=='POST':
            form = CheckoutForm(request.POST)
            pay_form=PaymentMethodForm(request.POST, instance=payment_obj)

        if form.is_valid() or pay_form.is_valid():
            name=form.cleaned_data.get('name')
            phone=form.cleaned_data.get('phone')
            email=form.cleaned_data.get('email')
            address=form.cleaned_data.get('address')
            order_note=form.cleaned_data.get('order_note')

            billing_address=Checkout(
                user=request.user,
                name=name,
                phone=phone,
                email=email,
                address=address,
                order_note=order_note,
            )
            billing_address.save()
            payment_obj=shipping_address=billing_address
            pay_method=pay_form.save()

            # Cash on delivery
            if pay_method.payment_option== 'Cash on delivery':
                order_qs= Order.objects.filter(user=request.user, ordered=False)
                order=order_qs[0]
                order.ordered=True
                order.payment_option=pay_method.payment_option

                order_items=Cart_product.objects.filter(user=request.user, ordered=False)

                for order_item in order_items:
                    order_item.ordered=True
                    order_item.save()
                order.save()
                messages.success(request, "Your order was successfull")

                return HttpResponseRedirect(reverse('index'))

            #SSlCommerz
            elif pay_method.payment_option=='SSL Commerce':
                store_id=settings.STORE_ID
                store_pass=settings.STORE_PASS
                mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=store_pass)
                status_url=request.build_absolute_uri(reverse('status'))
                mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

                order_qs=Order.objects.filter(user=request.user, ordered=False)
                order_items=order_qs[0].cart_product.all()
                order_item_count=order_qs[0].cart_product.count()
                order_total=order_qs[0].get_total()

                mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='FOOD', product_name=order_items, num_of_item=order_item_count, shipping_method='YES', product_profile='None')
                #customer profile information
                current_user=request.user
                mypayment.set_customer_info(name=current_user.username, email=email, address1=address, address2='demo2', city='Dhaka', postcode='1207', country='Bangladesh', phone=phone)

                mypayment.set_shipping_info(shipping_to=current_user.username, address=address, city='Dhaka', postcode='1209', country='Bangladesh')

                response_data = mypayment.init_payment()
                return redirect(response_data['GatewayPageURL'])
                return redirect('checkout')

@csrf_exempt
def sslc_status(request):
    if request.method=='post' or request.method=='POST':
        payment_data=request.POST
        status=payment_data['status']
        if status=='VALID':
            val_id=payment_data['val_id']
            tran_id=payment_data['tran_id']
            return HttpResponseRedirect(reverse('sslc_complete', kwargs={'val_id':val_id, 'tran_id':tran_id}))
    return render(request, 'index.html')


def sslc_complete(request, val_id, tran_id):
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    order=order_qs[0]
    order.ordered=True
    order.order_id=val_id
    order.payment_id=tran_id
    order.save()

    cart_items=Cart_product.objects.filter(user=request.user, ordered=False)
    for item in cart_items:
        item.ordered=True
        item.save()

    messages.success(request,"Your order was successfull")
    return redirect('index')



       

            



       

       

    

        
