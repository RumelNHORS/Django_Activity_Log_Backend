from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from .models import Product, ActivityLog

@receiver(post_save, sender=Product)
def log_product_save(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    ActivityLog.objects.create(user=instance.user, product=instance, action=action, timestamp=now())

@receiver(post_delete, sender=Product)
def log_product_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(user=instance.user, product=instance, action='DELETE', timestamp=now())
