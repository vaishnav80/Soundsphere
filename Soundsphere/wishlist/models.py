from django.db import models
from admin_panel.models import Product
from django.contrib.auth.models import User

class wishlist(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)


