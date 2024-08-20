from django.shortcuts import render,redirect
from django.contrib import messages
from admin_panel.models import Brand
from .models import *
from django.core.paginator import Paginator
from admin_panel.views import active_admin

@active_admin
def offer(req):

    return render(req,'offer.html')

@active_admin
def brand_offer(req):
    brand = Brand_offer.objects.all()
    context = {
        'brand' : brand
    }
    return render(req,'brand_offer.html',context)

@active_admin
def choose_brand(req):
    brand = Brand.objects.filter(is_active = True)
    context = {
        'brand' : brand
    }
    return render(req,'choose_brand.html',context)

@active_admin
def add_brand_offer(req,id):
    brand = Brand.objects.get(id = id)
    if Brand_offer.objects.filter(brand_id = brand).exists():
        messages.error(req,'the brand already had offer')
        return redirect(brand_offer)
    
    if req.method == 'POST':
        
        offer = req.POST['offer']
        if int(offer) > 100 or int(offer)<=0:
            messages.warning(req,'Invalid input !, offer percentage must be below 100')
            return redirect('add_brand_offer',id)
        obj = Brand_offer(offer = offer,brand_id = brand)
        obj.save()
        return redirect(brand_offer)
    
    context = {
        'brand':brand
    }
    return render(req,'add_brand_offer.html',context)

@active_admin
def edit_brand_offer(req,id):
    obj = Brand_offer.objects.get(id = id)
    if req.method == 'POST':
        offer = req.POST['offer']
        if int(offer) > 100 or int(offer)<=0:
            messages.warning(req,'Invalid input !, offer percentage must be below 100')
            return redirect('edit_brand_offer',id)
        obj.offer = offer
        obj.save()
        return redirect(brand_offer)

    context = {
        'obj':obj
    }

    return render(req,'edit_brand_offer.html',context)
        

def delete_brand_offer(req,id):
    obj = Brand_offer.objects.get(id = id)
    print(obj)
    obj.delete()
    return redirect(brand_offer)

@active_admin
def product_offer(req):
    product = Product_offer.objects.all()
    context = {
        'product' : product
    }
    return render(req,'product_offer.html',context)

@active_admin
def choose_product(req):
    product = Product.objects.filter(available = True)
    paginator = Paginator(product, 3) 
    
    page_number = req.GET.get('page') 
    page_obj = paginator.get_page(page_number) 
    context = {
        'page_obj' : page_obj
    }
    return render(req,'choose_product.html',context)

@active_admin
def add_product_offer(req,id):
    product = Product.objects.get(id = id)
    if Product_offer.objects.filter(product_id = product).exists():
        messages.error(req,'the product already had offer')
        return redirect(product_offer)
    if req.method == 'POST':
        offer = req.POST['offer']
        if int(offer) > 100 or int(offer)<=0:
            messages.warning(req,'Invalid input !, offer percentage must be below 100')
            return redirect('add_product_offer',id)
        obj = Product_offer(offer = offer,product_id = product)
        obj.save()
        return redirect(product_offer)
    
    context = {
        'product':product
    }
    return render(req,'add_product_offer.html',context)

@active_admin
def edit_product_offer(req,id):
    obj = Product_offer.objects.get(id = id)
    if req.method == 'POST':
        offer = req.POST['offer']
        if int(offer) > 100 or int(offer)<=0:
            messages.warning(req,'Invalid input !, offer percentage must be below 100')
            return redirect('edit_product_offer',id)
        now = obj.product_id.price / int(offer)
        now = obj.product_id.price - now
        obj.new_amount = now
        obj.offer = offer
        obj.save()
        return redirect(product_offer)

    context = {
        'obj':obj
    }

    return render(req,'edit_product_offer.html',context)
        

def delete_product_offer(req,id):
    obj = Product_offer.objects.get(id = id)
    print(obj)
    obj.delete()
    return redirect(product_offer)
