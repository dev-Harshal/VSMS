#Built-In Modules
import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
#User Defined Modules
#-----------------------------------------------------------------------------
# Create your models here.

class Users(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10,null=True,blank=True) #Validators
    ROLE = (('User','User'),('Staff','Staff'),('Admin','Admin'))
    role = models.CharField(max_length=10,choices=ROLE,default="User")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


class Enquiry(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField()
    contact_number = models.CharField(max_length=10,null=True,blank=True) #Validators
    message = models.CharField(max_length=200,null=True,blank=True)
    created_on = models.DateField(auto_now_add=True, null=True)
    ENQUIRY_STATUS = (('Active','Active'),('In Active','In Active'))
    status = models.CharField(max_length=10,choices=ENQUIRY_STATUS,null=True,blank=True,default="Active")


def generate_unique_number():
        while True:
            # Generate a random 9-digit number
            new_number = random.randint(100000000, 999999999)
            try:
                # Check if the generated number already exists
                Service.objects.get(service_number=new_number)
            except:
                # If the number doesn't exist, return it
                return new_number

class Service(models.Model):
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    service_number = models.IntegerField(default=generate_unique_number,unique=True,null=True,blank=True)
    CATEGORY_CHOICES = [
    ('2 Wheeler','2 Wheeler'),
    ('4 Wheeler','4 Wheeler'),
    ('Bus','Bus'),
    ('Truck','Truck')
]
    category = models.CharField(max_length=100,choices=CATEGORY_CHOICES,null=True,blank=True)
    vehicle_name = models.CharField(max_length=100,null=True,blank=True)
    vehicle_brand = models.CharField(max_length=100,null=True,blank=True)
    vehicle_reg_no = models.CharField(max_length=100,null=True,blank=True)
    service_time = models.TimeField(null=True,blank=True)
    service_date = models.DateField(null=True,blank=True)
    pickup_address = models.CharField(max_length=100,null=True,blank=True)
    need_delivery = models.BooleanField(default=False,null=True,blank=True)

    service_charge = models.IntegerField(null=True,blank=True,default=0)
    other_charge = models.IntegerField(null=True,blank=True,default=0)
    parts_charge = models.IntegerField(null=True,blank=True,default=0)
    total_amount = models.IntegerField(null=True,blank=True,default=0)

    payment_status = models.BooleanField(default=False)
    STATUS = [
    ("Pending","Pending"),
    ("In Process","In Process"),
    ("Work Complete","Work Complete"),
    ("Completed","Completed"),
    ("Delivered","Delivered")
]
    status = models.CharField(max_length=100,null=True,blank=True,choices=STATUS ,default="Pending")
    request_date = models.DateField(auto_now_add=True,null=True,blank=True)
    complete_date = models.DateField(null=True,blank=True)



class Notification(models.Model):
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE,null=True,blank=True)
    service_id = models.ForeignKey(Service,on_delete=models.CASCADE)
    NOTIFICATION_STATUS_CHOICES = [
    ('Booking Confirmed', 'Booking Confirmed'),
    ('In Process', 'In Process'),
    ('Payment', 'Payment'),
    ('Completed', 'Completed'),
    ('Delivered', 'Delivered'),
]
    status = models.CharField(max_length=100,choices=NOTIFICATION_STATUS_CHOICES,default="Booking Confirmed")
    created_on = models.TimeField(auto_now_add=True)