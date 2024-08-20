from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from admin_panel.models import Product
from .models import *
from .forms import ProductForm
from django.http import JsonResponse
from admin_panel.views import active_admin

@active_admin
def product_list(request):
    obj_list = Product.objects.all().order_by('id')  
    paginator = Paginator(obj_list, 3) 
    
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number) 
    
    return render(request, 'products.html', {'page_obj': page_obj})


def product_status(req, id):
    user = get_object_or_404(Product, id=id)
    user.available = not user.available
    user.save()
    return redirect(product_list)

@active_admin
def add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            price = cleaned_data.get('price')
            stock = cleaned_data.get('stock')
            print(stock)
            print(price)
            if price < 0 or stock < 0:
                return JsonResponse({'success': False, 'message': 'Invalid price or stock value.'}, status=400)
            else:
                form.save()
                return JsonResponse({'success': True, 'message': 'Product added successfully.'})
    else:
        
        form = ProductForm()
        
    return render(request,'add.html',{'form':form})

@active_admin
def add_images(req,id):
    obj = get_object_or_404(Product, pk=id)
    img = product_images.objects.filter(p_id = id)
    if req.method == 'POST':
        image = req.FILES.get('product_image')
        if image:
            obj = product_images(p_id = obj ,image = image)
            obj.save()
            return redirect(product_list) 
    
    return render(req,'add_image.html',{'obj':obj,'obj2':img})

@active_admin
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list') 
    else:
        form = ProductForm(instance=product)
    return render(request, 'add.html', {'form': form})