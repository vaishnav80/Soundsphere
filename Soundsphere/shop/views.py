from django.shortcuts import render,redirect
from admin_panel.models import *
from product.models import *
from .models import Cart
from django.contrib import messages
from django.db.models import *
from django.db.models.functions import Lower
from django.views.decorators.cache import never_cache
from user.views import signin
from offer.models import *
from reviews.models import Ratings
from django.db.models import Sum
from decimal import Decimal

def shop(req,id=0):
    default = Product.objects.all()
    brand = Brand.objects.filter(is_active =True)
    type = Type.objects.filter(is_active =True)
    connection = Connection_type.objects.filter(is_active =True)
    high = default.order_by('-price')
    low = default.order_by('price')
    colored = Product.objects.annotate(colors=Lower('color')).values('colors').distinct()
    new = default.order_by('created_at')
    a_z = Product.objects.annotate(a_z=Lower('name')).order_by('name')
    z_a = Product.objects.annotate(a_z=Lower('name')).order_by('-name')
    
    if id ==1:
        obj = high
    elif id ==2:
        obj = low
    elif id == 3:
        obj = new
    elif id == 4:
        obj = a_z
    elif id == 5:
        obj = z_a
    else:
        obj = default
    context = {
        'obj':obj,
        'brand':brand,
        'color' : colored,
        'type':type,
        'connection':connection 
    }
    return render(req,'shop.html',context)


def product_details(req,id):
    product = Product.objects.get(pk = id)
    product_img = product_images.objects.filter(p_id = id)
    offer = 0
    offer_rate = product.price
    if Brand_offer.objects.filter(brand_id = product.brand_id).exists():
        offer = Brand_offer.objects.get(brand_id = product.brand_id)
        print(offer.offer,product.price)
        product_price = int(product.price ) 
        offered = offer.offer
        offer_rate = product_price - (product_price *(offered/100))
    if Product_offer.objects.filter(product_id = product).exists():
        offer = Product_offer.objects.get(product_id = product)
        product_price = int(product.price ) 
        offered = offer.offer
        offer_rate = product_price - (product_price *(offered/100))
    stockcheck = 0
    obj = Product.objects.filter(brand_id = product.brand_id)
    if product.stock>0:
        stockcheck = 1
    count =0
    if req.user.is_authenticated:
        user_id=req.user
        count_userid = Cart.objects.filter(user_id=user_id).count()
        obj3 = Cart.objects.filter(Q(product_id = product) & Q(user_id=user_id))
        if obj3:
            messages.error(req,'**product already added in the cart')
            count =1

        if count_userid >= 3:
            messages.error(req,"**You cannot add more products to the cart. Maximum limit reached.")
            count =1
    if req.method =='POST':
        if req.user.is_authenticated:
            if count==0:
                if stockcheck>=1 and product.available:
                    obj = Cart(product_id = product,user_id = user_id,qty =1,rate = offer_rate)
                    obj.save()
                    return redirect('cart')
            
            else:
                return redirect('cart') 
        else:
            messages.warning(req,'please login first')
            return redirect(signin)
            
    rating = Ratings.objects.filter(product_id = product)
    star = rating.aggregate(Sum('stars'))['stars__sum'] or 0
    rating_count = rating.aggregate(Count('id'))['id__count'] or 0
    if rating_count>0:
        stars = str(star/rating_count)
    else:
        stars = 0
    context = {
        'product':product,
        'product_img':product_img,
        'obj':obj,
        'stockcheck':stockcheck,
        'count':count,
        'offer' : offer,
        'stars' : stars,
        'rating' :rating,
        'rating_count' : rating_count
    }   
    return render(req,'details.html',context)


def search(req):
    
    if req.method == 'GET':
       
        search = ''
        search = req.GET.get('search')
        obj = Product.objects.filter(name__icontains = search)
        brand = Brand.objects.filter(is_active =True)
        type = Type.objects.filter(is_active =True)
        connection = Connection_type.objects.filter(is_active =True)
        high = obj.order_by('-price')
        low = obj.order_by('price')
        colored = Product.objects.annotate(colors=Lower('color')).values('colors').distinct()
        new = obj.order_by('created_at')
        a_z = Product.objects.annotate(a_z=Lower('name')).order_by('name')
        z_a = Product.objects.annotate(a_z=Lower('name')).order_by('-name')
        
        if id ==1:
            obj = high
        elif id ==2:
            obj = low
        elif id == 3:
            obj = new
        elif id == 4:
            obj = a_z
        elif id == 5:
            obj = z_a
        else:
            obj = obj
        context = {
            'brand':brand,
            'color' : colored,
            'type':type,
            'connection':connection,
            'search' : search,
            'obj' : obj
        }
        return render(req,'shop.html',context)
        
    else:
        return redirect(shop)