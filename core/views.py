from django.shortcuts import render , redirect , get_object_or_404

from item.models import Category, Item

from .forms import SignupForm , OTPForm ,LoginForm

from django.contrib.auth import authenticate,login,logout

from .utils import send_otp

from datetime import datetime

from django.contrib.auth.models import User

from django.contrib import messages

import pyotp
        
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                send_otp(request)
                request.session['username'] = username
                print('ok, sending otp')
                return redirect('otp')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid user')
        # If form is not valid, or user is not authenticated, render the login page again
        return render(request, 'core/login.html', {'form': form})
    else:
        # If request method is not POST, render the login page with an empty form
        return render(request, 'core/login.html', {'form': form})




def index(request):
    items = Item.objects.filter(is_sold = False)
    categories = Category.objects.all()
    return render(request, 'core/index.html',
                {
                    'categories': categories,
                    'items':items,
                }  )

def otp_view(request):
    error_message = None
    form = OTPForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            otp=form.cleaned_data['otp']
            username = request.session['username']
            otp_secret_key = request.session.get['otp_secret_key']
            otp_valid_until = request.session.get['otp_valid_date']

            if otp_secret_key and otp_valid_until:
                valid_until = datetime.fromisoformat(otp_valid_until)
                if valid_until > datetime.now():
                    totp = pyotp.TOP(otp_secret_key, interval=60)
                    if totp.verify(otp):
                        user = get_object_or_404(User, username=username)
                        login(request, user)
                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']
                        return redirect ('/')
                    else:
                        error_message='Invalid one-time-password'
                else:
                    error_message = "One-time-password has expired"
            else:
                error_message = "UPS... something went wrong :("
        if error_message:messages.add_message(request, messages.ERROR , error_message)
    context = {'form':form}

    return render(request, 'otp.html', context)

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if(request.method == 'POST'):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html',
                  {
                      'form':form
                  })
def logout_view (request):
    logout(request)
    return redirect('/login/')
