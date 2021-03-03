from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator
from decimal import *
from django.conf import settings
from django.db.models.signals import post_save
from django.db import IntegrityError

from phonenumber_field.modelfields import PhoneNumberField

class InsufficientBalance(IntegrityError):
    """Raised when a wallet has insufficient balance to
    run an operation.
    We're subclassing from :mod:`django.db.IntegrityError`
    so that it is automatically rolled-back during django's
    transaction lifecycle.
    """

class UserProfileInfo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pic',blank=True)
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.user.username

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'phone_number'],
                name='unique_profile'
            )
        ]

    def change_profile_pic(self, pic):
        """Changes Profile Picture
        """
        self.profile_pic.delete(save = True)
        self.profile_pic = pic
        self.save()

class Wallet(models.Model):
    # We should reference to the AUTH_USER_MODEL so that
    # when this module is used and a different User is used,
    # this would still work out of the box.
    #
    # See 'Referencing the User model' [1]
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # This stores the wallet's current balance. Also acts
    # like a cache to the wallet's balance as well.
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default = 0, validators=[MinValueValidator(Decimal('0'))])

    # The date/time of the creation of this wallet.
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='unique_wallet'
            )
        ]

    def __str__(self):
        return self.user.username

    def deposit(self, value):
        """Deposits a value to the wallet.
        Also creates a new transaction with the deposit
        value.
        """
        self.current_balance += value
        self.save()

    def withdraw(self, value):
        """Withdraw's a value from the wallet.
        Also creates a new transaction with the withdraw
        value.
        Should the withdrawn amount is greater than the
        balance this wallet currently has, it raises an
        :mod:`InsufficientBalance` error. This exception
        inherits from :mod:`django.db.IntegrityError`. So
        that it automatically rolls-back during a
        transaction lifecycle.
        """
        if value > self.current_balance:
            raise InsufficientBalance('This wallet has insufficient balance.')

        self.current_balance -= value
        self.save()

    def transfer(self, wallet, value):
        """Transfers an value to another wallet.
        Uses `deposit` and `withdraw` internally.
        """
        self.withdraw(value)
        wallet.deposit(value)


class Wallet_Transaction(models.Model):
    # The wallet that holds this transaction.
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    # The value of this transaction.
    value = models.DecimalField(max_digits=10, decimal_places=2)

    # The value of the wallet at the time of this
    # transaction. Useful for displaying transaction
    # history.
    running_balance = models.DecimalField(max_digits=10, decimal_places=2)

    # The date/time of the creation of this transaction.
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null = True)

    def __str__(self):
        return self.wallet.user.username

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default = 0,validators=[MinValueValidator(Decimal('0.01'))])
    order_id = models.CharField(unique=True, max_length=500, null=True, blank=True)
    checksum = models.CharField(max_length=500, null=True, blank=True)
    success = models.BooleanField(default= False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['order_id'],
                name= 'unique_order'
            )
        ]

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id

#Creating Astrologers
class Astrologers(models.Model):

    LANGUAGE_LIST = [('Telugu', 'Telugu'), ("Tamil", 'Tamil'), ('Kannada', 'Kannada'), ('Malayalam', 'Malayalam'), ('Marathi', 'Marathi')]

    username = models.CharField(max_length = 30)
    name = models.CharField(max_length = 100)
    XP = models.FloatField(default = 0)
    language = models.CharField(max_length = 100, choices = LANGUAGE_LIST)
    phone_number = PhoneNumberField()
    profile_pic = models.ImageField(upload_to='astrologers_pic',blank=True)
    rate_per_min = models.FloatField(default = 20)

    approved = models.BooleanField(default= False)
    joined_on = models.DateTimeField(auto_now_add=True)

    class Meta:
       constraints = [
            models.UniqueConstraint(
                fields = ['username', 'phone_number'],
                name = 'Astro_unique'
            )
       ]

    def __str__(self):
       return self.username
