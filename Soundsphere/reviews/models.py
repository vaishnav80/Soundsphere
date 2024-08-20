from django.db import models

from admin_panel.models import Product
from django.contrib.auth.models import User


# Create your models here.

class Review(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    User_id  = models.ForeignKey(User,on_delete=models.CASCADE)
    comments = models.TextField()
    stars = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)


class Ratings(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    User_id  = models.ForeignKey(User,on_delete=models.CASCADE)
    comments = models.TextField()
    stars = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)