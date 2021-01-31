from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Wallet, Transaction, UserProfileInfo
#from payments.models import Transaction
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
from .forms import CreateUserForm, UserProfileInfoForm
from django.conf import settings
#from paypal.standard.forms import PayPalPaymentsForm

from PIL import Image
from .checksum import generate_checksum, verify_checksum

import os

def index(request):
    username = None
    if request.user:
        username = request.user.username
        return render(request, 'Home.html', {'username': username.capitalize()})
    return render(request, 'Home.html')

@login_required
def book(request):
    username = request.user.username
    return render(request, 'Book.html', {'username': username.capitalize()})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

#@login_required
#def user_wallet(request):
#    user = list(User.objects.filter(username = request.user).values())[0]
#    wallet = list(Wallet.objects.filter(user = request.user).values())[0]
#    context = {'username': user['username'].capitalize(), 'user': user, 'wallet': wallet}
#    if request.method == 'POST':
#        amount = int(request.POST.get('amount'))
#        transaction = Transaction.objects.create(made_by=request.user, amount=amount)
#        transaction.save()
#        request.session['order_id'] = transaction.id
#        return redirect(reverse('payments:process'))

#    return render(request, 'Wallet.html', context = context)

##################################################################################################

##################################################################################################

@csrf_exempt
@login_required
def initiate_payment(request):
    if request.method == "GET":
        user = list(User.objects.filter(username = request.user).values())[0]
        wallet = list(Wallet.objects.filter(user = request.user).values())[0]
        user_info = UserProfileInfo.objects.get(user = request.user)
        context = {'username': user['username'].capitalize(), 'user': user, 'wallet': wallet, 'info': user_info}
        return render(request, 'Wallet.html', context = context)
    if request.method == 'POST':
        print(list(User.objects.filter(username = request.user)))
        amount = int(request.POST.get('amount'))
        transaction = Transaction.objects.create(made_by=request.user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', str(os.environ['HOST']) + '/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
            transaction = get_object_or_404(Transaction, order_id = received_data['ORDERID'][0])
            wallet = get_object_or_404(Wallet, user = transaction.made_by)
            wallet.deposit(transaction.amount)
            transaction.success = True
            transaction.save()
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payments/callback.html', context=received_data)
        return render(request, 'payments/callback.html', context=received_data)

##################################################################################################

##################################################################################################

def register(request):
    registered = False
    if request.method == 'POST':
        wallet = Wallet()
        user_form = CreateUserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            print(request.FILES)
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            wallet.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            wallet.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
        return HttpResponseRedirect(reverse('Astro:user_login'))
    else:
        user_form = CreateUserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'register.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('login_user')
        password = request.POST.get('login_pass')
        user = authenticate(request, username = username, password = password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            messages.error(request, 'Either thy Username or Password is incorrect')
            return HttpResponseRedirect(reverse('Astro:user_login'))
    else:
        return render(request, 'login.html', {})
