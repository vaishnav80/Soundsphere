from django.shortcuts import render,redirect,get_object_or_404
from user_profile.models import User_address
from shop.models import Cart
from shop.views import product_details
from .models import Orders,items,shiped_address
from cart.views import cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import razorpay # type: ignore
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
from admin_panel.models import Product
from coupon.models import Coupon,user_coupons
from django.db.models import Q
from wallet.models import Wallet,Wallet_transaction
from offer.models import Product_offer,Brand_offer
import json
from user.views import signin
from wallet.views import active_user

@never_cache
@login_required
def checkout(req):
    user = req.user
    if user.is_active:
        carts = Cart.objects.filter(user_id = user)
        if carts.exists():
            for i in carts:
                if i.product_id.stock<=0 or i.product_id.available==False:
                    i.delete()
                    return redirect('details',id = i.product_id.id)
                elif i.product_id.stock<i.qty:
                    messages.warning(req,f'stock exceeded ,  please recheck {i.product_id.name} stock left {i.product_id.stock} only')
                    return redirect('cart')
            address= User_address.objects.filter(user_id = user)
            coupon = req.session.get('offer')
            coupon_code = req.session.get('coupon')
            a =req.session.get('address')
            msg = ''
            if a:
                msg = User_address.objects.get(id = a)
            lst = []
            for i in carts:
                if Product_offer.objects.filter(product_id = i.product_id).exists():
                    offer = Product_offer.objects.get(product_id = i.product_id)
                    product = Product.objects.get(name = i.product_id)
                    p = int(product.price)
                    o = offer.offer
                    last = p - (p*(o/100))
                    i.rate = last
                    i.save()
                    lst.append(last)
                elif Brand_offer.objects.filter(brand_id = i.product_id.brand_id).exists():
                    offer = Brand_offer.objects.get(brand_id = i.product_id.brand_id)
                    product = Product.objects.get(name = i.product_id)
                    p = int(product.price)
                    o = offer.offer
                    last = p - (p*(o/100))
                    i.rate = last
                    i.save()
                    lst.append(last)
                else:
                    p = int(i.product_id.price)
                    i.rate=p
                    i.save()
                    lst.append(p)

            context = {
                'address' : address,
                'cart' : carts,
                'option':msg,
                'coupon' : coupon,
                'lst' :json.dumps(lst),
                'coupon_code' : coupon_code
            }
            return render(req,'checkout.html',context)
        
        else:
            
            return redirect(cart)
    else:
        return redirect(signin)

def conform(req):
    user = req.user
    cart = Cart.objects.filter(user_id = user)
    add = req.session.get('address')
    grand = req.session.get('sub_total')
    offer = req.session.get('offer')
    if offer:
        grand = grand - offer
    if add == None:
        messages.error(req,'Choose a Address First')
        return redirect(checkout)
    address = User_address.objects.get(id =add)
    if req.method == 'POST':
        for i in cart:
            if i.product_id.stock<=0 or i.product_id.available==False:
                i.delete()
                return redirect('details',id = i.product_id.id)
            elif i.product_id.stock<i.qty:
                messages.warning(req,f'stock exceeded ,  please recheck {i.product_id.name} stock left {i.product_id.stock} only')
                return redirect('cart')
        payment = req.POST['paymentMethod']
        if payment == 'wallet':
            wallet = Wallet.objects.get(user_id = user)
            if wallet.balance < int(grand) :
                messages.warning(req,'insufficient balance in Wallet choose another payment option')
                return redirect(checkout)
            else:
                wallet.balance = wallet.balance - int(grand)
                wallet.save()
        
        addr = shiped_address(name = address.name , phone = address.phone , pincode = address.pincode,address = address.address , city = address.city, state = address.state )
        addr.save()
        
        obj = Orders(payment = payment , user_id = user ,status = Orders.pending,address_id = addr,grand_total = grand,)
        obj.save()
        req.session['order'] = obj.id
        if payment == 'Razorpay':
            return redirect(create_order)
        elif payment == 'wallet':
            wallet_transaction = Wallet_transaction(wallet_id = wallet , description = 'purchase',amount = grand ,balance = wallet.balance,order_id =obj )
            wallet_transaction.save()
        return redirect(successpage)
    return redirect(checkout)

def select_address(req):
    if req.method == 'POST':
        option = req.POST['deliveryAddress']
        req.session['address'] = option
        return redirect(checkout)
    return redirect(checkout)


def use_coupon(req):
    if req.method == 'POST':
        coupon = req.POST['coupon']
        user = req.user
        obj = Coupon.objects.filter(code=coupon).exists()
        today = timezone.now().date()
        if obj:
            i = Coupon.objects.get(code = coupon)
            if user_coupons.objects.filter(Q(user_id = user) & Q(coupon_id = i.id)).exists():
                sub_total = req.session.get('sub_total')
                if i.valid_to >=today and int(sub_total)>i.condition:
                    if  i.valid_from<=today:
                        obj = Coupon.objects.get(code = coupon)
                        req.session['coupon_id'] = obj.id
                        req.session['coupon'] = coupon
                        req.session['offer'] = i.offer
                        return redirect(checkout)
                    else:
                        messages.success(req,f'invalid coupon / coupon available from {i.valid_from}')
                        req.session['offer'] = 0
                        return redirect(checkout) 
                else:
                    messages.success(req,'invalid coupon / date expired')
                    return redirect(checkout) 
            else:
                messages.warning(req,'invalid coupon')

        else:
            messages.warning(req,'invalid coupon')        
            return redirect(checkout)
    return redirect(checkout)


def remove_coupon(req):
    req.session['offer'] = None
    req.session.pop('coupon_id',None)
    return redirect(checkout)


@active_user
def successpage(req):
    user = req.user
    cart = Cart.objects.filter(user_id = user)
    for i in cart:
        if i.product_id.stock<=0 or i.product_id.available==False:
            i.delete()
            return redirect('details',id = i.product_id.id)
        elif i.product_id.stock<i.qty:
            messages.warning(req,f'stock exceeded ,  please recheck {i.product_id.name} stock left {i.product_id.stock} only')
            return redirect('cart')
    coupon_id = req.session.get('coupon_id')
    grand = req.session.get('sub_total')
    offer = req.session.get('offer')
    if offer:
        grand = grand - offer
    order = req.session.get('order')
    obj = Orders.objects.get(id = order)
    user_coupon = user_coupons.objects.filter(Q(coupon_id = coupon_id) & Q(user_id = user.id))
    user_coupon.delete()
    
    for i in cart:
        obj5 = Product.objects.get(name = i.product_id)
        if obj5.stock>=i.qty:
            obj5.stock = obj5.stock - i.qty
            obj5.save()
            obj.total = obj.total + i.rate*i.qty
            obj.discount = obj.total - int(grand)
            obj.save() 
            item = items(product = i.product_id.name , rate = i.rate , qty = i.qty , order_id = obj ,total_rate = i.product_id.price)
            item.save()
            i.delete()
    obj.confirm = True
    obj.save()   
    req.session.pop('address',None)
    req.session.pop('offer',None)
    req.session.pop('total',None)
    req.session.pop('coupon_id',None)
    req.session.pop('order',None)
    return render(req,'conform.html')


def shop_address(req):
    user_id = req.user
    if req.method == 'POST':
        name = req.POST['name']
        phone = req.POST['phone']
        pincode = req.POST['pincode']
        locality = req.POST['locality']
        address = req.POST['address']
        city = req.POST['city']
        state = req.POST['state']
        landmark = req.POST['landmark']
        address_type = req.POST['address_type']

        obj = User_address(name =name,phone = phone,pincode = pincode,locality = locality,
                           address = address,city= city,state =state,landmark=landmark,address_type=address_type,user_id = user_id)
        obj.save()
        return redirect(checkout)
    

@active_user
def create_order(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    grand = request.session.get('sub_total')
    offer = request.session.get('offer')
    if offer:
        grand = grand - offer
    order_amount = grand *100
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    
    payment = client.order.create({
        'amount': order_amount,
        'currency': order_currency,
        'receipt': order_receipt,
        'payment_capture': '1'
    })

    context = {
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': payment['id'],
        'amount': order_amount,
        'currency': order_currency,
    }
    return render(request, 'payment.html', context)


from django.http import JsonResponse
@csrf_exempt
def save_subtotal(req):
    if req.method == 'POST':
        sub_total = req.POST.get('sub_total')
        req.session['sub_total'] = int(sub_total)
        return redirect('checkout')


