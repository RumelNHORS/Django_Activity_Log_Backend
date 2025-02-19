# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.utils.timezone import now
# from .models import Product, ActivityLog
# from .utils import get_current_user 

# # @receiver(post_save, sender=Product)
# # def log_product_save(sender, instance, created, **kwargs):
# #     action = 'CREATE' if created else 'UPDATE'
# #     ActivityLog.objects.create(user=instance.user, product=instance, action=action, timestamp=now())

# # @receiver(post_delete, sender=Product)
# # def log_product_delete(sender, instance, **kwargs):
# #     ActivityLog.objects.create(user=instance.user, product=instance, action='DELETE', timestamp=now())


# @receiver(post_save, sender=Product)
# def log_product_save(sender, instance, created, **kwargs):
#     action = 'CREATE' if created else 'UPDATE'
#     user = get_current_user()
#     if user:
#         ActivityLog.objects.create(user=user, product=instance, action=action, timestamp=now())

# @receiver(post_delete, sender=Product)
# def log_product_delete(sender, instance, **kwargs):
#     user = get_current_user()
#     if user:
#         ActivityLog.objects.create(user=user, product=instance, action='DELETE', timestamp=now())




from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from django.db import models
from decimal import Decimal
from datetime import datetime
from .models import Product, ProductPrice, ActivityLog
from .utils import get_current_user

TRACKED_MODELS = ['Product', 'ProductPrice'] 

def serialize_instance(instance):
    """Serialize model instance to a dictionary format."""
    data = {}
    for field in instance._meta.fields:
        value = getattr(instance, field.name)
        
        # Convert non-serializable types to JSON-friendly formats
        if isinstance(value, models.Model):
            value = str(value)  
        elif isinstance(value, Decimal):
            value = float(value)  
        elif isinstance(value, datetime):
            value = value.isoformat()
        
        data[field.name] = value
    return data

def log_activity(instance, action):
    user = get_current_user()
    if user:
        model_name = instance.__class__.__name__
        changes = {
            'fields': serialize_instance(instance)
        }
        ActivityLog.objects.create(
            user=user,
            model_name=model_name,
            action=action,
            timestamp=now(),
            changes=changes 
        )

@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    if sender.__name__ in TRACKED_MODELS:
        action = 'CREATE' if created else 'UPDATE'
        log_activity(instance, action)

@receiver(post_delete)
def log_model_delete(sender, instance, **kwargs):
    if sender.__name__ in TRACKED_MODELS:
        log_activity(instance, 'DELETE')
