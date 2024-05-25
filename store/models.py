from typing import Iterable
from django.db import models
from ckeditor.fields import RichTextField
from PIL import Image
from payment_app.models import *
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    
    verbose_name_plural = 'Categorys'
    
    name = models.CharField(max_length=50)
    parrent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    image=models.ImageField(upload_to="categoryImage/", blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img =Image.open(self.image)
        width, height = img.size
        target_width = 150
        #h_coefficient = width/600
        #target_height = height/h_coefficient
        target_height = 150
        img = img.resize((int(target_width), int(target_height)),Image.Resampling.LANCZOS)
        img.save(self.image.path, quality=50)
        img.close()
        self.image.close()
    
class Brand(models.Model):
    
    verbose_name_plural = 'Brands'

    name = models.CharField(max_length=50)
    icon=models.ImageField(upload_to="BrandsIcon/", blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img =Image.open(self.icon)
        width, height = img.size
        target_width = 50
        #h_coefficient = width/600
        #target_height = height/h_coefficient
        target_height = 50
        img = img.resize((int(target_width), int(target_height)),Image.Resampling.LANCZOS)
        img.save(self.icon.path, quality=20)
        img.close()
        self.icon.close()


    
class Banner(models.Model):
    name = models.CharField(max_length=50)
    image=models.ImageField(upload_to="bannerImage/", blank=True, null=True)
    url_link=models.URLField(max_length=500, blank=True, null=True)
    
    verbose_name_plural = 'Banners'

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name= models.CharField(max_length=200)
    image=models.ImageField(upload_to='ProductImage/')
    price=models.PositiveIntegerField()
    discount_price=models.PositiveBigIntegerField(blank=True, null=True)
    description=RichTextField()
    stock=models.IntegerField(blank=True, null=True)
    catagory=models.ForeignKey(Category, on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand, on_delete=models.CASCADE)

    verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    
    def get_review_list(self):
        review=ProductReview.objects.filter(product=self, approve_status=True)
        return review

    def get_avg_rating(self):
        review=review=ProductReview.objects.filter(product=self, approve_status=True)
        count=len(review)
        sum=0
        for i in review:
            sum +=i.rating

        if count != 0:
            return(sum*20/count)

    def get_rating_count(self):
        review=ProductReview.objects.filter(product=self, approve_status=True)
        count=len(review)
        return count
    

class Cart_product(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    total=models.PositiveIntegerField()

    def __str__(self):
        return self.product.name
    
   
    def total(self):
        if(self.product.discount_price):
            total1=self.quantity*self.product.discount_price
        else:
            total1=self.quantity*self.product.price
        return total1
    


class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    cart_product=models.ManyToManyField(Cart_product)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    shipping_address=models.ForeignKey(Checkout, on_delete=models.CASCADE, blank=True, null=True)
    PAYMENT_METHOD=(
        ('Cash on delivery', 'Cash on delivery'),
        ('SSL Commerce', 'SSL Commerce'),
    )
    payment_option=models.CharField(max_length=100, choices=PAYMENT_METHOD, blank=True, null=True)
    order_id=models.CharField(max_length=500, blank=True, null=True)
    payment_id=models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def get_total(self):
        add=0
        for i in self.cart_product.all():
            add+=i.total()
        return add
    

class ProductReview(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    created_on=models.DateTimeField(auto_now_add=True)
    RATING=(
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    rating=models.IntegerField(choices=RATING, default=5)
    review=models.TextField()
    image=models.ImageField(upload_to='ReviewImage/', blank=True, null=True)
    approve_status=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    
   
    

