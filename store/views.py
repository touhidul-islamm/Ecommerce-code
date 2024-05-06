from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    category=Category.objects.all()
    brand=Brand.objects.all()
    banner=Banner.objects.all()
    product=Product.objects.all()
    food_product=Product.objects.filter(catagory__name='Food')
    fashion_product=Product.objects.filter(catagory__name='fashion')

    context={
        'category': category,
        'brand': brand,
        'banner': banner,
        'product': product,
        'food_product':food_product,
        'fashion_product':fashion_product
    }
    return render(request,'index.html', context)


def product_details(request, pk):
    product_details=Product.objects.get(pk=pk)
    related_product=Product.objects.filter(Q(catagory__name=product_details.catagory.name)|Q(brand__name=product_details.brand.name)).exclude(pk=pk)
    context={
        'product_details': product_details,
        'related_product': related_product
    }
    return render(request, 'product_details.html', context)


def product_search(request):
    query=request.GET['q']
    product_search=Product.objects.filter(Q(name__icontains=query)|Q(catagory__name__icontains=query)|Q(brand__name__icontains=query))
    
    context={
        'product_search': product_search
    }
    return render(request, 'product_search.html', context)



@login_required(login_url='login')
def add_to_cart(request, pk):
    product=get_object_or_404(Product, pk=pk)
    cart_item, created=Cart_product.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.cart_product.filter(product__pk=product.pk).exists():
           cart_item.quantity +=1
           cart_item.save()
           messages.info(request, 'The product quantity is updated') 
           return redirect('product_details', pk=pk)
        else:
            order.cart_product.add(cart_item)
            messages.info(request, 'This item was add to cart')
            return redirect('product_details', pk=pk)
        
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.cart_product.add(cart_item)
        messages.info(request, 'This Item quantity was added')
        return redirect('product_details', pk=pk)
    

def cart_increment(request,pk):
    product=get_object_or_404(Product, pk=pk)
    cart_item, created=Cart_product.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.cart_product.filter(product__pk=product.pk).exists():
            cart_item.quantity +=1
            cart_item.save()
            messages.info(request, 'The product quantity is updated')
            return redirect('cart_summary')
        
    else:
        messages.info(request, 'This product quantity was updated')
        return redirect('cart_summary')
    

def cart_decriment(request,pk):
    product=get_object_or_404(Product, pk=pk)
    cart_item, created=Cart_product.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.cart_product.filter(product__pk=product.pk).exists():
            if cart_item.quantity>1:
                cart_item.quantity -=1
                cart_item.save()
                messages.info(request, 'This product quantity is removed')
                return redirect('cart_summary')
            else:
                cart_item.delete()
                messages.info(request, 'This product is deleted')
                return redirect('cart_summary')


    

def remove_cart(request,pk):
    product=get_object_or_404(Product, pk=pk)
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.cart_product.filter(product__pk=product.pk).exists():
            cart_item=Cart_product.objects.filter(user=request.user, ordered=False)[0]
            cart_item.delete()
            messages.info(request, 'this product is deleted')
            return redirect('cart_summary')
        
    else:
        messages.info(request, 'The product is empty')
        return redirect("/")
    

@login_required(login_url='login')
def cart_summary(request):
    try:
        order=Order.objects.get(user=request.user, ordered=False)
        context={
            'order':order
        } 
        return render(request, 'cart_summary.html', context)
    except ObjectDoesNotExist:
        messages.info(request, 'Your cart is empty') 
        return redirect('/')