from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Connection_type)
admin.site.register(Type)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Banner)
