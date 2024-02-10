from django.urls import path
from Staff.views import *
urlpatterns = [
    path('',staffHome,name="staff-home"),
    path('staff_login/',staffLogin,name="staff-login"),
    path('staff_logout/',staffLogout,name='staff-logout'),
    path('staff_profile/',staffProfile,name='staff-profile'),
    path('pending_reg/',pendingServiceReg,name='pending-reg'),
    path('in_process_reg/',inProgressServiceReg,name='in-process-reg'),
    path('completed_reg/',completedServiceReg,name='completed-reg'),
    path('delivered_reg/',deliveredServiceReg,name='delivered-reg'),
    path('enquiry/',enquiry,name='enquiry'),
    path('inactive_enquiry/',inactiveEnquiry,name='inactive-enquiry'),

]
