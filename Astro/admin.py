from django.contrib import admin
from .models import UserProfileInfo, Wallet, Transaction

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Wallet)

admin.site.register(Transaction)
