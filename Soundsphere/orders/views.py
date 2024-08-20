from django.shortcuts import render,redirect
from checkout.models import Orders
from cart.models import *
from checkout.models import Orders,items,shiped_address
from admin_panel.models import Product
from wallet.models import Wallet,Wallet_transaction
from admin_panel.views import active_admin
from wallet.views import active_user

@active_admin
def admin_order(req):
    order = Orders.objects.all().order_by('-id')
    
    context= {
        'order' : order
    }
    return render(req,'admin_orders.html',context)

@active_admin
def order_manage(req,id):
    obj = items.objects.filter(order_id = id)
    address = Orders.objects.get(id = id)
    context = {
        'obj':obj,
        'address':address
    }
    return render(req,'ordermanage.html',context)

@active_admin
def change_order_status(req,id,status):
    order = Orders.objects.get(id = id)
    dummy_amount =0
    if status == 'canceled':
        obj = items.objects.filter(order_id = id)
        if not order.payment == 'Cash On Delivery':
            for i in obj:
                if i.product_status == True:
                    obj5 = Product.objects.get(name = i.product)
                    obj5.stock = obj5.stock + i.qty
                    obj5.save()
                    dummy_amount = dummy_amount + i.qty*i.rate

                order.status = status
                order.save()
                wallet = Wallet.objects.get(user_id = order.user_id) 
                a = dummy_amount-order.discount
                wallet.balance += a
                wallet.save()
                wallet_transaction = Wallet_transaction(wallet_id = wallet , description = 'Order canceled by admin',amount = a ,balance = wallet.balance,order_id =order )
                wallet_transaction.save()

            return redirect(admin_order)
        else:
            for i in obj:
                if i.product_status == True:
                    obj5 = Product.objects.get(name = i.product)
                    obj5.stock = obj5.stock + i.qty
                    obj5.save()

                order.status = status
                order.save()
            return redirect(admin_order)
    else:
        order.status = status
        order.save()
        return redirect(admin_order)