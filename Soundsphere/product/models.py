from django.db import models

from admin_panel.models import Product

class product_images(models.Model):
    p_id = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_id')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)