from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Checkout(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    phone=models.CharField(max_length=15)
    email=models.EmailField()
    address=models.CharField(max_length=200)
    order_note=models.TextField(max_length=200)

    def __str__(self):
        return self.name 