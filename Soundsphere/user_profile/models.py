from django.db import models

from django.contrib.auth.models import User


class User_details(models.Model):
    first_name = models.CharField(max_length=100,null=True,blank=True)
    second_name = models.CharField(max_length=100,null=True,blank=True)
    user_id = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    refferal_code = models.CharField(max_length=10,default='123456',blank=True)

    


class User_address(models.Model):
    HOME = 'home'
    OFFICE = 'office'
    ADDRESS_TYPE_CHOICES = [
        (HOME, 'Home'),
        (OFFICE, 'Office'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    pincode = models.CharField(max_length=6)
    locality = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,default=13    )
    def __str__(self):
        return self.name
