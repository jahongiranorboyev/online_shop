from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from apps.newsletter.models import Subscriber

@shared_task
def send_mail_task():
    if Subscriber.objects.exists():
        subscribers = Subscriber.objects.all()
        subject = 'Good morning!'
        message = 'Have a good day!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [subscriber.email for subscriber in subscribers]
        send_mail(subject, message, from_email, recipient_list)
    else:
        print("No subscribers to send email to.")