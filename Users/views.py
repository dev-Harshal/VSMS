#Built-In Modules
from django.shortcuts import render,redirect
from django.urls import reverse 
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, logout
import re
from django.db.models import Q

from Users.data import UserHomeData
#User Defined Modules
from .models import *
from .mail import create_notification, send_mail_to_the_user
from .decorators import user_custom_login_required
#-----------------------------------------------------------------------------
# Create your views here.
def format_license_plate(input_str):
    # Define the pattern for the desired format
    pattern = re.compile(r'^[A-Z]{2}\s?\d{2}\s?[A-Z]{2}\s?\d{4}$')

    # Check if the input matches the desired format
    if pattern.match(input_str):
        # If it matches, keep it the same
        return input_str
    else:
        # If not, try to reformat it
        formatted_str = re.sub(r'[^A-Z0-9]', '', input_str.upper())
        if len(formatted_str) == 10:
            return f"{formatted_str[:2]} {formatted_str[2:4]} {formatted_str[4:6]} {formatted_str[6:]}"
        else:
            return None

def index(request):
    if request.method == 'POST':
        first_name = str(request.POST.get('first_name')).title()
        last_name = str(request.POST.get('last_name')).title()
        email = str(request.POST.get('email')).lower()
        contact_number = request.POST.get('contact_number')
        message = request.POST.get('message')
        enquiry = Enquiry(name=f"{first_name} {last_name}",email=email,contact_number=contact_number,message=message)
        enquiry.save()
        message = f"""
            Hello {str(first_name).title()}
            Thank You for Contacting MOTORA, Customer support team will contact you shortly. Thank you!
            MOTORA    
            """
        send_mail_to_the_user(email,message)
        messages.add_message(request, messages.INFO, "Support team will contact you shortly. Thank you!")
        return redirect (reverse('index') + '#contact')
    else:
        return render(request,'index.html')

def registerUser(request):
    if request.method == 'POST':
        first_name = str(request.POST.get('first_name')).title()
        last_name = str(request.POST.get('last_name')).title()
        email = str(request.POST.get('email')).lower()
        username = email
        phone_number = str(request.POST.get('phone_number'))
        password = str(request.POST.get('password'))
        confirm_password = str(request.POST.get('confirm_password'))

        user = Users.objects.filter(email=email).first()
        if user:
            messages.add_message(request, messages.ERROR, "Email already exists")
            return redirect(reverse('register'))
        if password!= confirm_password:
            messages.add_message(request, messages.WARNING, "Passwords do not match")
            return redirect(reverse('register'))
        user = Users(first_name=first_name, last_name=last_name, email=email,username=username, 
                    password=password,phone_number=phone_number)
        user.save()
        message = f"""
                    Welcome {str(first_name).capitalize()}:
                    Thank You for Registering with MOTORA.
                    MOTORA    
                    """
        send_mail_to_the_user(email,message)
        return redirect(reverse('login'))
    else:
        return render(request,'register.html')

def loginUser(request):
    if request.method == 'POST':
        email = str(request.POST.get('email')).lower()
        password = str(request.POST.get('password'))
        user = Users.objects.filter(email=email).first()
        if user:
            if user.role == 'Staff':
                messages.add_message(request, messages.ERROR, "Invalid Email or Password")
                return redirect(reverse('login'))
            if user.check_password(password):
                login(request,user)
                return redirect(reverse('home'))
            else:
                messages.add_message(request, messages.ERROR, "Invalid Email or Password")
                return redirect(reverse('login')) 
        else:
            messages.add_message(request, messages.ERROR, "Invalid Email or Password")
            return redirect(reverse('login'))
    else:
        return render(request, 'login.html')
@user_custom_login_required
def logoutUser(request):
    logout(request)
    return redirect(reverse('login'))

@user_custom_login_required
def home(request):
    if request.method == 'POST':
        notification = Notification.objects.filter(user_id=request.user.id).all()
        notification.delete()
        next_url = request.path  # Get the current path
        return redirect(f'{next_url}')
    notification = Notification.objects.filter(user_id=request.user.id).all()
    context = {'home':UserHomeData(request.user.id)}
    return render(request,'home.html',context=context)

@user_custom_login_required
def userProfile(request):
    if request.method == 'POST':
        action = request.POST.get('action','password')
        user = Users.objects.filter(id=request.user.id).first()
        if action == 'update_profile':
            first_name = str(request.POST.get('first_name',user.first_name)).title()
            last_name = str(request.POST.get('last_name',user.last_name)).title()
            email = str(request.POST.get('email',user.email)).lower()
            phone_number = str(request.POST.get('phone_number',user.phone_number))
            
            if request.user.email == email or not Users.objects.filter(email=email).exists():
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.phone_number = phone_number
                user.save()
                messages.add_message(request, messages.INFO, "Profile Updated Successfully")
                return redirect(reverse('profile'))
            else: 
                messages.add_message(request, messages.ERROR, "Email Exists")
                return redirect(reverse('profile'))
        else:
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')

            if user.check_password(old_password):
                if new_password == confirm_new_password:
                    user.set_password(new_password)
                    user.save()
                    login(request,user)
                    messages.add_message(request, messages.INFO, "Password Updated Successfully")
                    return redirect(reverse('profile'))
                else:
                    messages.add_message(request, messages.ERROR, "Passwords do not match")
                    return redirect(reverse('profile'))
            else:
                messages.add_message(request, messages.ERROR, "Old password does not match")
                return redirect(reverse('profile'))
    else:
        return render(request,'profile.html')


@user_custom_login_required
def contact(request):
    if request.method == 'POST':
        name = str(request.POST.get('name')).title()
        email = str(request.POST.get('email')).lower()
        contact_number = request.POST.get('contact_number')
        message = request.POST.get('message')
        enquiry = Enquiry(name=name,email=email,contact_number=contact_number,message=message)
        enquiry.save()
        message = f"""
            Hello {str(name).title()}
            Thank You for Contacting MOTORA, Customer support team will contact you shortly. Thank you!
            MOTORA    
            """
        send_mail_to_the_user(email,message)
        messages.add_message(request, messages.INFO, "Support team will contact you shortly. Thank you!")
        return redirect (reverse('contact'))
    else:    
        return render(request,'contact.html')

@user_custom_login_required
def bookService(request):
    if request.method == 'POST':
        user_id = Users.objects.filter(id=request.user.id).first()
        category = str(request.POST.get('category'))
        vehicle_name = str(request.POST.get('vehicle_name')).title()
        vehicle_brand = str(request.POST.get('vehicle_brand')).title()
        vehicle_reg_no = str(request.POST.get('vehicle_reg_no'))
        service_time = request.POST.get('service_time')
        service_date = request.POST.get('service_date')
        pickup_address = str(request.POST.get('pickup_address'))
        need_delivery = str(request.POST.get('need_delivery'))

        vehicle_reg_no = format_license_plate(str(vehicle_reg_no))
        if vehicle_reg_no == None:
            messages.add_message(request, messages.ERROR, "Invalid Vehicle Registration Number")
            return redirect('book_service')
        
        if need_delivery == 'True':
            need_delivery = True
        else:
            need_delivery = False

        service = Service(user_id=user_id,category=category,vehicle_name=vehicle_name,vehicle_brand=vehicle_brand,
                          vehicle_reg_no=vehicle_reg_no,service_time=service_time,service_date=service_date
                          ,pickup_address=pickup_address,need_delivery=need_delivery)
        service.save()
        message = f"""
        Service Request for Vehicle No.:{service.vehicle_reg_no} Confirmed.
        Service Number : {service.service_number}
        Date : {service.service_date}
        Time : {str(service.service_time).upper()}

        MOTORA    
        """
        send_mail_to_the_user(str(user_id.email),message)
        create_notification(request.user,service,'Booking Confirmed')
        return redirect(reverse('in_process'))
    else:
        return render(request,'service.html')
        
@user_custom_login_required
def in_process(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        service = Service.objects.filter(id=id).first()
        service.payment_status = True
        create_notification(request.user,service,'Payment')
        service.save()
        message = f"""
        Payment Recieved.
        Vehicle No : {service.vehicle_reg_no.upper()}
        Service Number : {service.service_number}
        Total Amount : {service.total_amount}

        MOTORA    
        """
        send_mail_to_the_user(service.user_id.email,message)
        return redirect(reverse('in_process'))

    services = Service.objects.filter(Q(user_id=request.user.id) & ~ Q(status = "Delivered"))
    context = {'services': services}
    return render(request,'in_process.html', context=context)


@user_custom_login_required
def delivered(request):
    services = Service.objects.filter(Q(user_id=request.user.id) & Q(status = "Delivered"))
    context = {'services': services}
    return render(request,'delivered.html', context=context)