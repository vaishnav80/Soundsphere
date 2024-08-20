from django.shortcuts import render,redirect
from .models import Ratings
from user_profile.views import orders
from admin_panel.models import Product
from admin_panel.views import active_admin
from wallet.views import active_user

@active_admin
def admin_review(req):
    rating = Ratings.objects.all()
    context = {
        'rating' : rating
    }
    return render(req,'admin_review.html',context)

@active_user
def user_review(req):
    rating = Ratings.objects.filter(User_id = req.user)
    context = {
        'rating' : rating
    }
    return render(req,'user_review.html',context)


def add_review(req,id):
    if req.method == 'POST':
        star = req.POST['rating']
        comment = req.POST['comment']
        id = Product.objects.get(name =id)
        obj = Ratings(product_id = id,stars = star,comments = comment,User_id = req.user)
        obj.save()
        return redirect(orders)

    context= {
        'id': id
    }
    return render(req,'add_review.html',context)


def delete_review(req,id,id2):
    obj = Ratings.objects.get(id = id)
    obj.delete()
    if id2 == 1:
        return redirect(user_review)
    return redirect()