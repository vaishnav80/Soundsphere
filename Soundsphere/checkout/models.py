from django.db import models

from shop.models import Cart
from user_profile.models import User_address
from django.contrib.auth.models import User


class shiped_address(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    pincode = models.CharField(6)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,default=13)

class Orders(models.Model):
    pending = 'pending'
    success = 'success'
    canceled = 'canceled'
    choices = [
        (pending,'pending'),
        (success, 'success'),
        (canceled,'canceled')
    ]
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    payment = models.CharField(max_length=50)
    status = models.CharField(max_length=30,choices=choices)
    order_date = models.DateField(auto_now_add=True)
    grand_total = models.IntegerField(default=0)
    address_id = models.ForeignKey(shiped_address,on_delete=models.CASCADE,default=1)
    total = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    confirm = models.BooleanField(default=False)


class items(models.Model):
    product = models.CharField(max_length=50,default='a')
    rate = models.IntegerField(default=0)
    qty = models.IntegerField(default=0)
    total_rate = models.IntegerField(default=0)
    order_id = models.ForeignKey(Orders,on_delete=models.CASCADE)
    product_status = models.BooleanField(default=True)


    
    
    