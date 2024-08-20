from django.shortcuts import render,redirect
from django.http import JsonResponse
from admin_panel.models import *
from .models import wishlist
from user.views import signin
from shop.views import product_details
from django.contrib import messages
from django.db.models import Q

def wish(req):
    if req.user.is_authenticated and req.user.is_active:  
        obj2 = wishlist.objects.filter(user_id = req.user)
        context = {
            'obj2':obj2
        }
        
        return render(req,'wishlist.html',context)
    else:
        messages.warning(req,'please login first')
        return redirect(signin)

def add_to_wishlist(req):
    
    if req.user.is_active and not req.user.is_authenticated:
        if req.method == 'POST':
            user = req.user
            id = req.POST.get('product_id')
            product = Product.objects.get(id = id)
            if wishlist.objects.filter(Q(product_id= product) & Q(user_id = user)).exists():
                return JsonResponse({'warning': True})
            else:
                wish = wishlist(product_id = product , user_id = user)
                wish.save()
            return JsonResponse({'success': True, 'product_name': 'Product Name'}) 
    

        return JsonResponse({'success': False})
    else:
        return redirect(signin)
    
def wish_remove(req,id):
    
    obj = wishlist.objects.get(id = id)
    obj.delete()
    return redirect(wish)

def addw(req,id):
    if req.user.is_active and req.user.is_authenticated: 
        user = req.user
        product = Product.objects.get(id = id)
        if wishlist.objects.filter(product_id= product).exists():
            return redirect(wish)
        wishes = wishlist(product_id = product , user_id = user)
        wishes.save()
        return redirect(wish)
    else:
        messages.warning(req,'please login first')
        return redirect(signin)
    