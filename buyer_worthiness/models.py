from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length= 100, blank=True, null=True)
    staff_id = models.CharField(max_length=12, unique=True)


class Buyer_Analysis(models.Model):
    name = models.CharField(max_length = 180)
    submited_at = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    completed = models.BooleanField(default = False, blank = True)
    worthy = models.BooleanField(default = False, blank = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, blank = True, null = True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bank_name = models.CharField(max_length=20, blank=True, null=True)
    bank_statement = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True)
    monthly_payment = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.name