# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Inventory

@receiver(post_save, sender=Inventory)
def check_reorder_level(sender, instance, **kwargs):
    if instance.current_stock <= instance.reorder_level:
        # Trigger a reorder alert (e.g., send an email)
        send_mail(
            'Reorder Alert',
            f'The stock for {instance.product.name} has reached or gone below the reorder level. Current stock: {instance.current_stock}.',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )