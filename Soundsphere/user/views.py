from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import *
import smtplib
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import secrets
from datetime import datetime
from django.contrib import messages
from admin_panel.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache
import os
from dotenv import load_dotenv # type: ignore
from wishlist.models import wishlist
from user_profile.models import User_details
from wallet.models import Wallet,Wallet_transaction


def Home(req): 
    obj = Banner.objects.all()
    obj2 = Product.objects.all()
    wish = 0
    if req.user.is_active:
        user = req.user
        wish = wishlist.objects.filter(user_id = user)
    context = {
        'obj':obj,
        'obj2':obj2,
        'wish' : wish
    }
    return render(req,'index.html',context)


@never_cache
def signin(req):
    if req.user.is_active:
        if req.user.is_staff:
            logout(req)
            return redirect(signin)
        else:
            return redirect('profile')
    else:
        if req.method == 'POST':
            username = req.POST['username']
            password = req.POST['password']
            try:
                obj = User.objects.get(username = username)
            except User.DoesNotExist:
                messages.error(req, 'Username is invalid')
                return redirect(signin)
            if obj.is_active:
                user = authenticate(username = username ,password = password)
                if user:
                    login(req,user)
                    wallet = Wallet.objects.get(user_id = user)
                    if Wallet_transaction.objects.filter(description = 'Joining bonus').exists():
                        return redirect('profile')
                    else:
                        return redirect(refferal_code)
                else:
                    messages.error(req, 'Invalid password')
                    return redirect(signin) 
            else:
                messages.error(req, 'User blocked by Admin')
                return redirect(signin) 

        return render(req,'signin.html')


def signout(req):
    logout(req)
    return redirect("/")

def signup(request):
    if request.user.is_active:
        return redirect('profile')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            refferal_code = request.POST['refferal_code']
            emails = email
            obj2 = User.objects.filter(username = username)
            obj  = User.objects.filter(email =emails)
            if obj or obj2:
                messages.error(request, 'Email or username  already exist ')
                return redirect('signup')
            if not User_details.objects.filter(refferal_code = refferal_code).exists():
                messages.error(request, 'Inavalid refferal Code' )
                return redirect('signup')
            request.session['username'] = username
            request.session['password'] = password
            request.session['email'] = email
            request.session['refferal_code'] = refferal_code
            otp = secrets.token_hex(3)
            expires_at = timezone.now() + timedelta(minutes=5)
            request.session['otp'] = otp
            request.session['otp_expires_at'] = expires_at.isoformat()
            load_dotenv()

            to =email
            smtp_server = 'smtp.gmail.com'
            port = 587 
            sender_email ="vaishnavpuzhakkal3@gmail.com"
            password = "xevd spjc clmr vnmj" 

            receiver_email = to
            try:
                server = smtplib.SMTP(smtp_server, port)
                server.ehlo()  # Can be omitted
                server.starttls(context=None)  # Secure the connection
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, f'Your OTP code is {otp} , otp will expiry in 5 minutes')
                print("Email sent successfully")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                server.quit()
                return redirect('otp_verification')
        
        
        return render(request,'signup.html')

def otp_verification_view(request):
    if request.method == 'POST':
            otp_code = request.POST['otp']
            stored_otp = request.session.get('otp')
            otp_expires_at = request.session.get('otp_expires_at')

            if not stored_otp or not otp_expires_at:
                (None, 'OTP session data not found')
            else:
                otp_expires_at = datetime.fromisoformat(otp_expires_at)

                
                if otp_code == stored_otp:
                    if timezone.now() > otp_expires_at:
                        messages.error(request,f'{otp_code}, OTP has expired')
                        return redirect(otp_verification_view)
                    username = request.session.get('username')
                    if username:
                        password = request.session.get('password')
                        user = User(
                            username=username,
                            email=request.session.get('email'),
                        )
                        user.set_password(password)
                        user.save()
                        request.session.pop('username', None)
                        request.session.pop('passsword', None)
                        request.session.pop('email', None)
                        request.session.pop('otp', None)
                        request.session.pop('user_info', None)
                        request.session.pop('otp_expires_at', None)

                        return redirect('signin')
                    else:
                        messages.error(request,'User session data not found')
                        return redirect(otp_verification_view)
                       
                else:
                    messages.error(request,' Invalid OTP')
                    return redirect(otp_verification_view)
                    


    return render(request, 'otp_verification.html')



def forgot_password(req):
    if req.method == 'POST':
            email = req.POST['email']
            req.session['email'] = email
            # Generate OTP
            otp = secrets.token_hex(3)
            expires_at = timezone.now() + timedelta(minutes=5)
            req.session['otp'] = otp
            req.session['otp_expires_at'] = expires_at.isoformat()
            load_dotenv()
            to = email
            smtp_server = 'smtp.gmail.com'
            port = 587  # For starttls
            sender_email = "vaishnavpuzhakkal3@gmail.com"
            password = "xevd spjc clmr vnmj"  # App password

            receiver_email = to
            try:
                server = smtplib.SMTP(smtp_server, port)
                server.ehlo()  # Can be omitted
                server.starttls(context=None)  # Secure the connection
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, f'Your OTP code for change password is {otp} , otp will expiry in 5 minutes')
                print("Email sent successfully")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                server.quit()
            return redirect(otp_verification_forgotpassword)
    

    return render(req,'forgotpassword.html')


def otp_verification_forgotpassword(request):
    if request.method == 'POST':
        print('sds')
    
        otp_code = request.POST['otp']
        stored_otp = request.session.get('otp')
        otp_expires_at = request.session.get('otp_expires_at')

        if not stored_otp or not otp_expires_at:
            messages.error(request, 'OTP session data not found')
            return redirect(otp_verification_forgotpassword)
        else:
            otp_expires_at = datetime.fromisoformat(otp_expires_at)

            if timezone.now() > otp_expires_at:
                messages.error(request, 'OTP has expired')
                return redirect(otp_verification_forgotpassword)
            elif otp_code == stored_otp:
                email = request.session.get('email')
                obj=User.objects.get(email = email)
                print(obj)
                if obj:
                    
                    request.session.pop('otp', None)
                    
                    request.session.pop('otp_expires_at', None)

                    return redirect('resetpassword',)
                else:
                    messages.error(request, 'User session data not found')
                    return redirect(otp_verification_forgotpassword)
            else:
                messages.error(request, 'invalid otp')
                return redirect(otp_verification_forgotpassword)

    return render(request, 'forgot_otpverification.html')


def reset_password(request):
    if request.method == 'POST':
        form = resetpassword(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']

            email = request.session.get('email')
            if email:
                try:
                    user = User.objects.get(email=email)
                    user.set_password(new_password)
                    user.save()

                    # Clear session
                    request.session.pop('email', None)

                    messages.success(request, 'Your password has been reset successfully.')
                    return redirect('signin')
                except User.DoesNotExist:
                    messages.error(request, 'No user associated with this email.')
            else:
                messages.error(request, 'Session expired or invalid session data.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = resetpassword()
    return render(request,'reset.html',{'form':form})

def refferal_code(req):
    user = req.user
    refferal = req.session.get('refferal_code')
    try:
        obj = User_details.objects.get(refferal_code =refferal)
        wallet = Wallet.objects.get(user_id = obj.user_id)
        wallet.balance = wallet.balance + 500
        wallet.save()
        w_t = Wallet_transaction(wallet_id = wallet,description = 'refferal bonus',amount = 500,balance = wallet.balance)
        w_t.save()
        wallet2 = Wallet.objects.get(user_id = user)
        wallet2.balance = wallet2.balance+200
        wallet2.save()
        w_t2 = Wallet_transaction(wallet_id = wallet2,description = 'Joining bonus',amount = 200,balance = wallet2.balance)
        w_t2.save()
    except:
        obj = None
    return redirect('profile')

def regenerate_otp(req,id):
    email = req.session.get('email')

    otp = secrets.token_hex(3)
    expires_at = timezone.now() + timedelta(minutes=5)
    req.session['otp'] = otp
    req.session['otp_expires_at'] = expires_at.isoformat()
    load_dotenv()

    to =email
    smtp_server = 'smtp.gmail.com'
    port = 587 
    sender_email ="vaishnavpuzhakkal3@gmail.com"
    password = "xevd spjc clmr vnmj" 

    receiver_email = to
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=None)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, f'Your OTP code is {otp} , otp will expiry in 5 minutes')
        print("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()
        if id ==1:
            return redirect('otp_verification')
        elif id==2:
            return redirect(otp_verification_forgotpassword)
