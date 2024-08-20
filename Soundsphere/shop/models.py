from django.db import models
from admin_panel.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.IntegerField()
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)



