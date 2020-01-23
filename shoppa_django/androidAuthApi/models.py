from django.db import models
from shoppy.models import Buyer

# Create your models here.

class ShortCode(models.Model):
    short_code = models.CharField(max_length=10,null=False, blank=False)
    phone_number = models.CharField(max_length=20,null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
