from django.core.mail import send_mail
from django.conf import settings

from Users.models import Notification

def send_mail_to_the_user(recipient,message):
    subject = f'MOTORA'

    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [recipient])

def create_notification(user,service,status):
    notification = Notification.objects.create(user_id = user,
        service_id = service , status = status
    )
    notification.save()