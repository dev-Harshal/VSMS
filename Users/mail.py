from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
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


def send_sms(message,phone):

    try:
        account_sid = 'AC44b0558f1032fb33207097505510c296'
        auth_token = '860f321e1aab40fd366cf4957824f0d0'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
        from_ ='+19413402507',
        body=message,
        to= f'+91{phone}'
        )

        print(message.sid)
    except:
        pass