from django.shortcuts import render,redirect
from .forms import *
from admin_panel.models import *
from admin_panel.views import active_admin

@active_admin
def addbanner(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        product_id = request.POST.get('product_id')
        image = request.FILES.get('image')
        if name and product_id and image:
            product = Product.objects.get(id=product_id)
            new_image = Banner(name=name, product_id=product, image=image)
            new_image.save()
            return redirect(banner)
    products = Product.objects.all()
    return render(request,'addbanner.html',{'products': products})

@active_admin
def banner(req):
    
    obj = Banner.objects.all()
    return render(req,'banner.html',{'obj':obj,})

def delete_banner(req,id):
    obj = Banner.objects.get(pk = id)
    obj.delete()
    
    return redirect(banner)