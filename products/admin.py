from django.contrib import admin
from products import models as product_models
# Register your models here.


admin.site.register(product_models.ActivityLog)
admin.site.register(product_models.Product)