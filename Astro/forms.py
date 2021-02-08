from django.contrib.auth.models import User
from django import forms
from captcha.fields import ReCaptchaField

from .models import UserProfileInfo, Wallet, Astrologers, Transaction
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password')

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password')
        if password:
            try:
                validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password', error)

class UserProfileInfoForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta():
        model = UserProfileInfo
        fields = ('profile_name','profile_pic', 'phone_number','captcha',)

class WalletForm(forms.ModelForm):
    class Meta():
        model = Transaction
        fields = ('amount'),

class AstrologerProfileInfoForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta():
        model = Astrologers
        fields = ('name', 'XP','phone_number', 'language', 'rate_per_min', 'profile_pic', 'captcha')

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        XP = self.cleaned_data.get('XP')
        rate = self.cleaned_data.get('rate_per_min')

        if XP < 0:
            self.add_error('XP', ValidationError('Invalid Experience', code = 'invalid'))
        if rate <= 0:
            self.add_error('rate_per_min', ValidationError("Don't you wanna earn money here.", code = 'invalid'))
