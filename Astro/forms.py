from django.contrib.auth.models import User
from django import forms

from .models import UserProfileInfo, Wallet, Astrologers

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','email','password',)

class UserProfileInfoForm(forms.ModelForm):
     class Meta():
         model = UserProfileInfo
         fields = ('profile_name','profile_pic',)

class AstrologerProfileInfoForm(forms.ModelForm):
     class Meta():
         model = Astrologers
         fields = ('username','name', 'XP','phone_number', 'language', 'rate', 'rate_per_min', 'profile_pic',)
