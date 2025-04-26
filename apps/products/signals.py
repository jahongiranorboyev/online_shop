from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.newsletter.models import Subscriber
from apps.products.models import Product
from apps.newsletter.views import send_newsletter


@receiver(post_save, sender=Product)
def send_email_new_product(instance,created,**kwargs):
        if created:
                send_newsletter()
