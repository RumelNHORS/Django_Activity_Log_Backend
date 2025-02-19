# from django.db import models
# from django.contrib.auth.models import User




# class Product(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name



# class ActivityLog(models.Model):
#     ACTION_CHOICES = [
#         ('CREATE', 'Create'),
#         ('UPDATE', 'Update'),
#         ('DELETE', 'Delete'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
#     action = models.CharField(max_length=10, choices=ACTION_CHOICES)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user} {self.action} {self.product.name} on {self.timestamp}"



from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    effective_date = models.DateTimeField()

    def __str__(self):
        return f"{self.product.name} - {self.price} on {self.effective_date}"

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    model_name = models.CharField(max_length=255)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField()  # Use django.db.models.JSONField

    def __str__(self):
        return f"{self.user} {self.action} {self.model_name} on {self.timestamp}"