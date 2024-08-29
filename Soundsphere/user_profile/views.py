from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from checkout.models import Orders,items,shiped_address
from checkout.views import checkout,get_coordinates,calculate_distance
from admin_panel.models import Product
from django.db.models import *
from wallet.models import Wallet,Wallet_transaction
from django.db.models import Count
from wallet.views import active_user
import razorpay # type: ignore
from django.conf import settings
from datetime import date
from django.http import JsonResponse
from django.urls import reverse
import json
from offer.models import Product_offer,Brand_offer

@active_user
def profile(req):
    if req.session.session_key:
        a = req.user.username
        obj = User.objects.get(username = a)
        obj2 = User_details.objects.get(user_id = obj)
        if req.method == 'POST':
            fname = req.POST['name']
            lname = req.POST['lname']
            phone = req.POST['phone']
            obj2.first_name = fname
            obj2.second_name = lname
            obj2.phone = phone
            obj2.save()
            return redirect(profile)
        
        # if obj.first_name=='':
        #     messages.error(req, 'User blocked by Admin')
        #     return redirect(profile)
        context = {
            'id' : obj,
            'obj' : obj2
        }
        return render(req,'profile.html',context)

@active_user
def add_photo(req):
    a = req.user.username
    obj = User.objects.get(username = a)
    obj2 = User_details.objects.get(user_id = obj)
    if req.method=='POST':
        image = req.FILES.get('product_image')
        obj2.profile_photo = image
        obj2.save()
        return redirect(profile)
    return render(req,'profile_photo.html')

@active_user
def address(req):
    user = req.user
    obj = User_address.objects.filter(user_id = user)

    return render(req,'address.html',{'obj':obj})


@active_user
def addaddress(req):
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
        return redirect('address')
    return render(req,'createaddress.html')


def deleteaddress(req,id):
    obj = User_address.objects.get(pk=id)
    obj.delete()
    return redirect('address')

@active_user    
def editaddress(req,num,id):
    obj = User_address.objects.get(pk=id)
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

        obj.name = name
        obj.phone = phone
        obj.pincode = pincode
        obj.landmark = landmark
        obj.locality = locality
        obj.city = city
        obj.address =address
        obj.state = state
        obj.address_type =address_type


        api_key = 'AIzaSyA8PfqSoNTFsKTIryi5TCJTomzQMV_RETU'
        pincode1 = '673634'
        pincode2 = pincode
        lat2, lng2 = get_coordinates(pincode2, api_key)

        if lat2==1:
            messages.error(req,'invalid pincode')
            return redirect(editaddress,num,id)
        else:
            obj.name =name
            obj.phone = phone
            obj.pincode = pincode
            obj.locality = locality
            obj.address = address
            obj.city= city
            obj.state =state
            obj.landmark=landmark
            obj.address_type=address_type
            obj.save()
            print(obj)
            if num==1:
                return redirect('address')
            else:
                return redirect(checkout)
    return render(req,'editaddress.html',{'obj':obj})

@active_user
def orders(req):
    user = req.user
    order = Orders.objects.filter(user_id =user).order_by('-id')
    today = date.today()
    for i in order:
        if i.order_date != today and i.confirm == False:
            i.status = 'canceled'
            i.save()
    context= {
        'order' : order,
        'today' : today
    }
    return render(req,'orders.html',context)

@active_user
def ordered_product(req,id):
    obj = items.objects.filter(order_id = id)
    count = items.objects.filter(Q(product_status=True) & Q(order_id = id)).aggregate(count=Count('id'))['count']
    if count>1:
        count = True
    else:
        count = False
    address = Orders.objects.get(id = id)
    context = {
        'obj':obj,
        'address':address,
        'count': count
    }
    return render(req,'ordered_product.html',context)

@active_user
def change_status(req,id,status,product):
    user = req.user
    dummy_amount = 0
    order = Orders.objects.get(id = id)
    if status in dict(Orders.choices).keys():
        if product  == 'nothing' :
            if  (order.payment == 'Cash On Delivery' and order.status =='success') or (not order.payment == 'Cash On Delivery'):
                obj = items.objects.filter(order_id = id)
                for i in obj:
                    if i.product_status == True:
                        obj5 = Product.objects.get(name = i.product)
                        obj5.stock = obj5.stock + i.qty
                        obj5.save()
                        dummy_amount = dummy_amount + i.qty*i.rate
                        print(i.qty*i.rate,dummy_amount)

                
                wallet = Wallet.objects.get(user_id = user) 
                a = dummy_amount-order.discount
                a = a + order.delivery
                wallet.balance += a
                wallet.save()
                if order.status == 'success':
                    wallet_transaction = Wallet_transaction(wallet_id = wallet , description = 'Order returned by You',amount = a ,balance = wallet.balance,order_id =order )
                    wallet_transaction.save()
                else:
                    wallet_transaction = Wallet_transaction(wallet_id = wallet , description = 'Order canceled by You',amount = a ,balance = wallet.balance,order_id =order )
                    wallet_transaction.save()
                order.status = status
                order.save()
            else:
                obj = items.objects.filter(order_id = id)
                for i in obj:
                    if i.product_status == True:
                        obj5 = Product.objects.get(name = i.product)
                        obj5.stock = obj5.stock + i.qty
                        obj5.save()
                order.status = status
                order.save()
        else:
            obj = items.objects.get(Q(product = product) & Q(order_id = order))
            obj5 = Product.objects.get(name = product) 
            if  (order.payment == 'Cash On Delivery' and order.status =='success') or (not order.payment == 'Cash On Delivery'):
                    wallet = Wallet.objects.get(user_id = user)
                    wallet.balance = wallet.balance + (obj.qty*int(obj.rate))
                    wallet.save()
                    if order.status=='success':
                        wallet_transaction = Wallet_transaction(wallet_id = wallet , description = 'Order returned by You',amount = obj.qty*obj.rate ,balance = wallet.balance,order_id =order )
                        wallet_transaction.save()
                    else:
                        wallet_transaction = Wallet_transaction(wallet_id = wallet , description = 'Order canceled by You',amount = obj.qty*obj.rate ,balance = wallet.balance,order_id =order )
                        wallet_transaction.save()
            obj5.stock = obj5.stock + obj.qty
            obj.product_status = False
            obj.save()
            obj5.save()
            return redirect(orders)
    return redirect(orders)


def retry_order(request):
    data = json.loads(request.body)
    id = data.get('id')
    obj = Orders.objects.get(id= id)
    item = items.objects.filter(order_id = id)
    for i in item:
        product = Product.objects.get(name = i.product)
        if Product_offer.objects.filter(product_id = product).exists():
            offer = Product_offer.objects.get(product_id = product)
            p =int( product.price-( (product.price) * offer.offer /100))
            print(i.rate , p)
            if i.rate!=p:
                obj.status = 'canceled'
                obj.save()
                return JsonResponse({'status': 'error', 'message': 'Product price mismatched. Order canceled.'}, status=400)
        else:
            if i.rate!= product.price:
                obj.status = 'canceled'
                obj.save()
                return JsonResponse({'status': 'error', 'message': 'Product price mismatched. Order canceled.'}, status=400)
        if product.stock<=0 or product.available==False or product.stock<i.qty:
            obj.status = 'canceled'
            obj.save()
            return JsonResponse({'status': 'error', 'message': 'Product out of stock. Order canceled.'}, status=400)
        
    amount = obj.grand_total *100
    request.session['order'] = id
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order_amount = amount
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'
    payment = client.order.create({
        'amount': order_amount,
        'currency': order_currency,
        'receipt': order_receipt,
        'payment_capture': '1'
    })
    
    
    # Return the necessary details as JSON
    return JsonResponse({
        'status': 'success',
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': payment['id'],
        'amount': order_amount,
        'currency': order_currency,
        'callback_url': request.build_absolute_uri(reverse('successpage')),
        'redirect_url': request.build_absolute_uri(reverse('failure')),
    })