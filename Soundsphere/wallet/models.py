from django.db import models
from django.contrib.auth.models import User
from checkout.models import Orders

class Wallet(models.Model):

    balance = models.IntegerField(blank=True,default=0)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)


class Wallet_transaction(models.Model):
    wallet_id = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    amount = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    order_id = models.ForeignKey(Orders,on_delete=models.CASCADE,blank=True,null=True)
