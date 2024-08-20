from django.shortcuts import render,redirect,get_object_or_404

from django.contrib import messages
from admin_panel.models import *
from admin_panel.views import active_admin

@active_admin
def category(req):
    return render(req,'category.html')

@active_admin
def brand(req):
    brand = Brand.objects.all()
    return render(req,'brand.html',{'obj':brand})

@active_admin
def connection(req):
    obj = Connection_type.objects.all()
    return render(req,'connection.html',{'obj':obj})

@active_admin
def types(req):
    obj = Type.objects.all()
    return render(req,'types.html',{'obj':obj})

@active_admin
def brand_status(req, id):
    user = get_object_or_404(Brand, id=id)
    user.is_active = not user.is_active
    user.save()
    return redirect(brand)

@active_admin
def type_status(req, id):
    user = get_object_or_404(Type, id=id)
    user.is_active = not user.is_active
    user.save()
    return redirect(types)

@active_admin
def connection_status(req, id):
    user = get_object_or_404(Connection_type, id=id)
    user.is_active = not user.is_active
    user.save()
    return redirect(connection)

@active_admin
def addtypes(req):
    if req.method == 'POST':
        type = req.POST['typename']
        active = req.POST['isActive']
        brand = Type.objects.all()
        for i in brand:
            if i.type ==type:
                messages.error(req, 'this type already exist')
                return redirect(addbrand)
        if active=='active':
            a = True
        else:
            a = False
        obj = Type(type = type ,is_active = a)
        obj.save()
        return redirect(types)
    return render(req,'addtype.html')

@active_admin
def addconnection(req):
    if req.method == 'POST':
        type = req.POST['name']
        active = req.POST['isActive']
        brand = Connection_type.objects.all()
        for i in brand:
            if i.name ==type:
                messages.error(req, 'this connection already exist')
                return redirect(addconnection)
        if active=='active':
            a = True
        else:
            a = False
        obj = Connection_type(name = type ,is_active = a)
        obj.save()
        return redirect(connection)
    return render(req,'addconnection.html')

@active_admin
def addbrand(req):
    if req.method == 'POST':
        name = req.POST['name']
        active = req.POST['isActive']
        brand = Brand.objects.all()
        for i in brand:
            if i.name.lower() ==name.lower():
                messages.error(req, ' this Brand already exist')
                return redirect(addbrand)
        if active=='active':
            a = True
        else:
            a = False
        obj = Brand(name = name ,is_active = a)
        obj.save()
        return redirect('brand')
    return render(req,'addbrand.html')