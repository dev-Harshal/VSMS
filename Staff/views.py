import datetime
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from Staff.data import StaffHomeData1, staffHomeData
from Users.decorators import staff_custom_login_required
from Users.mail import create_notification, send_mail_to_the_user
from Users.models import Enquiry, Service, Users
from django.db.models import Q
# Create your views here.

@staff_custom_login_required
def staffHome(request):
    return render(request,'staff_home.html',context={'data':staffHomeData(),'home':StaffHomeData1()})


def staffLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.role == 'User':
                messages.add_message(request, messages.ERROR, "Invalid Email or Password")
                return redirect(reverse('staff-login'))
            else:
                login(request, user)
                return redirect(reverse('staff-home'))
        else:
            messages.add_message(request, messages.ERROR, "Email or Password Invalid")
            return redirect(reverse('staff-login'))

    return render(request,'staff_login.html')

@staff_custom_login_required
def staffLogout(request):
    logout(request)
    return redirect(reverse('staff-login'))

@staff_custom_login_required
def staffProfile(request):
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
                return redirect(reverse('staff-profile'))
            else: 
                messages.add_message(request, messages.ERROR, "Email Exists")
                return redirect(reverse('staff-profile'))
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
                    return redirect(reverse('staff-profile'))
                else:
                    messages.add_message(request, messages.ERROR, "Passwords do not match")
                    return redirect(reverse('staff-profile'))
            else:
                messages.add_message(request, messages.ERROR, "Old password does not match")
                return redirect(reverse('staff-profile'))
    else:
        return render(request,'staff_profile.html')
    
@staff_custom_login_required
def pendingServiceReg(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        service = Service.objects.filter(id=service_id).first()
        service.status = 'In Process'
        create_notification(service.user_id,service,'In Process')
        service.save()
        return redirect(reverse('in-process-reg'))
    services = Service.objects.filter(status='Pending').all()
    return render(request,'pending_req.html',context = {'services':services})

@staff_custom_login_required
def inProgressServiceReg(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'bill':
            service_id = request.POST.get('service_id')
            service = Service.objects.filter(id=service_id).first()
            service.parts_charge = int(request.POST.get('parts_charge',0)) + service.parts_charge
            service.service_charge = int(request.POST.get('service_charge',0)) + service.service_charge
            service.other_charge = int(request.POST.get('other_charge',0)) + service.other_charge
            total = int(request.POST.get('parts_charge',0)) + int(request.POST.get('other_charge',0)) + int(request.POST.get('service_charge',0))
            service.total_amount = int(service.total_amount) + total
            service.save()
            return redirect(reverse('in-process-reg'))
        elif request.POST.get('action') == 'proceed':
            service_id = request.POST.get('service_id')
            service = Service.objects.filter(id=service_id).first()
            service.status = 'Completed'
            message = f"""
        Work Completed.
        Vehicle No : {service.vehicle_reg_no.upper()}
        Service Number : {service.service_number}
        -------------------------------------------
        Bill Amount : {service.total_amount}

        MOTORA    
        """
            send_mail_to_the_user(service.user_id.email,message)
            create_notification(service.user_id,service,'Completed')
            service.save()
            return redirect(reverse('completed-reg'))
        else:
            service_id = request.POST.get('service_id')
            service = Service.objects.filter(id=service_id).first()
            service.status = 'Work Completed'
            create_notification(service.user_id,service,'Work Completed')
            service.save()
            return redirect(reverse('in-process-reg'))
    services = Service.objects.filter(Q(status="In Process") | Q(status="Work Completed")).all()
    return render(request,'in_process_reg.html',context = {'services':services})

@staff_custom_login_required
def completedServiceReg(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'payment':
            service_id = request.POST.get('service_id')
            service = Service.objects.filter(id=service_id).first()
            service.payment_status = True
            message = f"""
        Payment Recieved.
        Vehicle No : {service.vehicle_reg_no.upper()}
        Service Number : {service.service_number}
        Total Amount : {service.total_amount}

        MOTORA    
        """
            send_mail_to_the_user(service.user_id.email,message)
            create_notification(request.user,service,'Payment')
            service.save()
            return redirect(reverse('completed-reg'))
        else:
            service_id = request.POST.get('service_id')
            service = Service.objects.filter(id=service_id).first()
            service.status = 'Delivered'
            service.complete_date = datetime.datetime.now()
            create_notification(service.user_id,service,'Delivered')
            message = f"""
        Vehicle Delivered.
        Vehicle No : {service.vehicle_reg_no.upper()}
        Service Number : {service.service_number}

        Thank You for choosing your Service.

        MOTORA    
        """
            send_mail_to_the_user(service.user_id.email,message)
            service.save()
            return redirect(reverse('delivered-reg'))
    services = Service.objects.filter(status='Completed').all()
    return render(request,'completed_reg.html',context = {'services':services})

@staff_custom_login_required
def deliveredServiceReg(request):
    services = Service.objects.filter(status='Delivered').all()
    return render(request,'delivered_reg.html',context={'services':services})


@staff_custom_login_required
def enquiry(request):
    if request.method == 'POST':
        enquiry_id = request.POST.get('enquiry_id')
        enquiry = Enquiry.objects.filter(id=enquiry_id).first()
        enquiry.status = 'In Active'
        enquiry.save()
        return redirect(reverse('inactive-enquiry'))
    enquirys = Enquiry.objects.filter(status="Active")
    return render(request,'enquiry.html',context={'enquirys':enquirys})



@staff_custom_login_required
def inactiveEnquiry(request):
    if request.method == 'POST':
        enquiry_id = request.POST.get('enquiry_id')
        enquiry = Enquiry.objects.filter(id=enquiry_id).first()
        enquiry.status = 'Active'
        enquiry.save()
        return redirect(reverse('enquiry'))
    enquirys = Enquiry.objects.filter(status="In Active")
    return render(request,'inactive_enquiry.html',context={'enquirys':enquirys})