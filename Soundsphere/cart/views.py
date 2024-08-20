from django.shortcuts import render,redirect
import json
from shop.views import product_details
from django.views.decorators.cache import never_cache
from shop.models import Cart
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib import messages
from user.views import *
from coupon.models import Coupon
from offer.models import Product_offer,Brand_offer

@never_cache
def cart(req):
    if req.user.is_active and req.user.is_authenticated:
        user = req.user
        
        obj = Cart.objects.filter(user_id = user)
        length = len(obj)
        lst = []
        for i in obj:
            if Product_offer.objects.filter(product_id = i.product_id).exists():
                offer = Product_offer.objects.get(product_id = i.product_id)
                product = Product.objects.get(name = i.product_id)
                p = int(product.price)
                o = offer.offer
                last = p - (p*(o/100))
                lst.append(last)
            elif Brand_offer.objects.filter(brand_id = i.product_id.brand_id).exists():
                offer = Brand_offer.objects.get(brand_id = i.product_id.brand_id)
                product = Product.objects.get(name = i.product_id)
                p = int(product.price)
                o = offer.offer
                last = p - (p*(o/100))
                lst.append(last)
            else:
                p = int(i.product_id.price)
                lst.append(p)
        context = {
            'obj' : obj,
            'lst' :json.dumps(lst),
            'len': length
            
        }
        req.session.pop('total',None)
        return render(req,'cart.html',context)
    else:
        messages.warning(req,'please login first')
        return redirect(signin)

def remove(req,id):
    obj = Cart.objects.get(pk = id)
    obj.delete()
    return redirect(cart)

@csrf_exempt
def update_quantity_ajax(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        new_quantity = request.POST.get('quantity')
        try:
            product = get_object_or_404(Cart, id=product_id)
            if product.product_id.stock >= int(new_quantity):
                product.qty = int(new_quantity)
                product.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient stock'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



    

