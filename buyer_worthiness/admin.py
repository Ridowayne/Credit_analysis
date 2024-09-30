from django.contrib import admin
from .models import CustomUser, Buyer_Analysis

# Register CustomUser model
admin.site.register(CustomUser)

# Register Buyer_Analysis model
admin.site.register(Buyer_Analysis)
