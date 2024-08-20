from django.db import models

from coupon.models import Coupon
from  checkout.models import Orders


class Sales_report(models.Model):
    coupon_id = models.ForeignKey(Coupon,on_delete=models.CASCADE)
    offer = models.IntegerField()
    order_id = models.ForeignKey(Orders,on_delete=models.CASCADE),
    created_at = models.DateField(auto_now_add=True)