from django.shortcuts import render,redirect
from .models import Wallet,Wallet_transaction
from functools import wraps
from user.views import signin
from django.contrib import messages

def active_user(func):
    @wraps(func)
    def _wrapped_view(req, *args, **kwargs):
        if req.user.is_active==True and req.user.is_authenticated:
            return func(req, *args, **kwargs)
        else:
            messages.warning(req,'please login first')
            return redirect(signin)
    return _wrapped_view

@active_user
def wallet(req):
        user = req.user
        wallet = Wallet.objects.get(user_id = user)
        transaction = Wallet_transaction.objects.filter(wallet_id = wallet).order_by('-date')
        context = {
            'wallet' : wallet,
            'transaction' : transaction
        }
        return render(req,'wallet.html',context)