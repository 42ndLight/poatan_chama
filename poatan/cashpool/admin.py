from django.contrib import admin
from .models import Chama, CashPool

# Registering Models to admin site 
admin.site.register(Chama)
admin.site.register(CashPool)