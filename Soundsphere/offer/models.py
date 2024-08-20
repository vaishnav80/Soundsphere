from django.db import models


from admin_panel.models import Brand,Product

class Brand_offer(models.Model):
    brand_id = models.ForeignKey(Brand,on_delete=models.CASCADE)
    offer = models.IntegerField()
    new_amount = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)


class Product_offer(models.Model):
    product_id = models.ForeignKey(Product,on_delete= models.CASCADE)
    offer = models.IntegerField()
    new_amount = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)