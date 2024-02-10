from Users.models import Notification,Service,Enquiry
from django.db.models import Q

def message_processor(request):
    notification = Notification.objects.filter(user_id=request.user.id).all()[::-1]
    service = Service.objects.all()
    user_p = service.filter(~Q(status="Delivered") & Q(user_id=request.user.id)).all().count()
    user_d = service.filter(Q(status="Delivered") & Q(user_id=request.user.id)).all().count()
    enquiry = Enquiry.objects.filter(status="Active").all().count()
    numbers = {'pending':service.filter(status='Pending').count(),
               'process':service.filter(Q(status="In Process") | Q(status="Work Completed")).all().count(),
               'completed':service.filter(status='Completed').count,
               'delivered':service.filter(status='Delivered').count(),
               'all':service.filter(status="Delivered").count(),
               'enquiry':enquiry,
               'user_p':user_p,
               'user_d':user_d}
    
    return {'notification': notification,'id': request.user.id,'numbers': numbers}



    