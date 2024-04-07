from django.shortcuts import render
from .models import *
from django.db.models import Q

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
