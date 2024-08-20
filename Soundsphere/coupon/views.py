from django.shortcuts import render,redirect
from .models import Coupon,user_coupons
import random
import string
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from user_profile.models import User_details
from django.contrib import messages
from datetime import datetime, date
from admin_panel.views import active_admin
from wallet.views import active_user

def generate_coupon_code(length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

@active_admin
def coupon(req):
    obj = Coupon.objects.all().order_by('-id')
    context = {
        'obj' : obj
    }
    return render(req,'coupon.html',context)

@active_user
def user_coupon(req):
    user = req.user
    obj = User_details.objects.get(user_id = user)
    if obj.refferal_code=='' or obj.refferal_code == '123456':
        obj.refferal_code = generate_coupon_code(7)
        obj.save()
    refferal_code = obj.refferal_code
    today = timezone.now().date()
    user_coupon = user_coupons.objects.filter(user_id = user)
    for i in user_coupon:
        if i.coupon_id.valid_to < today - timedelta(days=3):
            i.delete()
    
    context = {
        'obj': user_coupon,
        'refferal_code' :refferal_code
    } 
    return render(req,'coupon_user.html',context)


@active_admin
def add_coupon(req):
    if req.method == 'POST':
        code = generate_coupon_code(10)
        description = req.POST['description']
        offer = req.POST['offer']
        condition = req.POST['upto']
        expiry = req.POST['expiry']
        valid_from = req.POST['valid_from']
        today = timezone.now().date()
        expiry = datetime.strptime(expiry, "%Y-%m-%d").date()
        valid_from = datetime.strptime(valid_from, "%Y-%m-%d").date()
        if expiry <today or int(offer)<0:
            messages.error(req,'Invalid input expiry date must be an upcoming date also offer must be a positive amount')
            return redirect(add_coupon)
        elif valid_from<today or expiry<valid_from:
            messages.error(req,'Invalid input check the dates...')
            return redirect(add_coupon)
        coupon = Coupon(code = code , description = description , valid_to = expiry , condition = condition , offer = offer ,valid_from = valid_from)
        coupon.save()
        user = User.objects.all()
        for i in user:
            obj = user_coupons(user_id = i, coupon_id = coupon)
            obj.save()

        return redirect('coupon')
    return render(req,'add_coupon.html')

@active_admin
def edit_coupon(req,id):

    coupons = Coupon.objects.get(id = id)
    if req.method == 'POST':
        description = req.POST['description']
        offer = req.POST['offer']
        condition = req.POST['upto']
        expiry = req.POST['expiry']
        valid_from = req.POST['valid_from']
        coupons.description = description
        coupons.offer = offer
        coupons.condition = condition
        coupons.valid_to = expiry
        coupons.valid_from = valid_from
        today = timezone.now().date()
        expiry = datetime.strptime(expiry, "%Y-%m-%d").date()
        valid_from = datetime.strptime(valid_from, "%Y-%m-%d").date()
        if expiry <today or int(offer)<0:
            messages.error(req,'Invalid input expiry date must be an upcoming date also offer must be a positive amount')
            return redirect(edit_coupon)
        elif valid_from<today or expiry<valid_from:
            messages.error(req,'Invalid input check the dates...')
            return redirect(edit_coupon)
        coupons.save()
        return redirect(coupon)
    context = {
        'coupon' : coupons
    }
    return render(req,'add_coupon.html',context)


def delet_coupon(req,id):
    coupon = Coupon.objects.get(id = id)

    coupon.delete()
    return redirect('coupon')

