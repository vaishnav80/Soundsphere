from django.db import models
from django.contrib.auth.models import User



class Coupon(models.Model):
    code = models.CharField(max_length=10,unique=True,blank=True)
    description = models.CharField(max_length=200)
    valid_from = models.DateField(auto_now_add=True)
    valid_to = models.DateField(blank=True)
    offer = models.IntegerField(default=0)
    condition = models.IntegerField(default=0)


class user_coupons(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    coupon_id = models.ForeignKey(Coupon,on_delete=models.CASCADE)
  

    