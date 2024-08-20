from django.db import models
from django.utils import timezone


class Connection_type(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Type(models.Model):
    type =  models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.type

class Brand(models.Model):
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    color = models.CharField(max_length=30)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    tags = models.CharField(max_length=30)
    brand_id = models.ForeignKey('Brand',on_delete=models.CASCADE,related_name='brand_name',default=1)
    type_id = models.ForeignKey('type',on_delete=models.CASCADE,related_name='type_name',default=1)
    connection_id = models.ForeignKey('Connection_type',on_delete=models.CASCADE,related_name='connection',default=1)
    created_at = models.DateTimeField(default=timezone.now) 
    
    def __str__(self):
        return self.name
    

    


class Banner(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Banner/',blank=True,null=True)
    product_id = models.ForeignKey('Product',on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.name
    

