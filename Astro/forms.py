from django.contrib.auth.models import User
from django import forms
from captcha.fields import ReCaptchaField
from django.contrib.auth.forms import PasswordChangeForm

from .models import UserProfileInfo, Wallet, Astrologers, Transaction
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password', 'email', 'first_name', 'last_name')

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

class ModifyUserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(ModifyUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control input-value', 'placeholder': "First Name", 'autocomplete' : 'off'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control input-value', 'placeholder': "Last Name", 'autocomplete' : 'off'})

    def save(self, commit=True):
        changes = super(ModifyUserForm, self).save(commit=False)
        self.user.first_name = changes.first_name
        self.user.last_name = changes.last_name
        return self.user

class ModifyUserPasswordForm(PasswordChangeForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control input-value', 'placeholder': "Old Password", 'autocomplete' : 'off'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control input-value', 'placeholder': "New Password", 'autocomplete' : 'off'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control input-value', 'placeholder': "New Password", 'autocomplete' : 'off'})


    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        #user = User.objects.get(username = self.username)
        print(password)
        self.user.set_password(password)
        self.user.save()
        return self.user

class ProfilePicForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.attrs.update({'class': 'form-control input-value', 'placeholder': "Update Picture", 'autocomplete' : 'off'})


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
        fields = ('name', 'XP','phone_number', 'language', 'rate_per_min', 'profile_pic', 'captcha',)

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
