from django.contrib import admin
from .models import *
# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','email','role','is_superuser')
admin.site.register(Users,UsersAdmin)

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','contact_number','message','created_on','status')
admin.site.register(Enquiry,EnquiryAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_number','category','vehicle_reg_no','status',)
admin.site.register(Service,ServiceAdmin)
admin.site.register(Notification)
