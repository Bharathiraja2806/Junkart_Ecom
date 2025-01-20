from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Customer
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '' and password == '':
            messages.info(request, "Pls enter username or password!")
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            messages.info(request, "Login failed , Pls try again!")
    return render(request, 'accountsapp/login.html')

def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')

        if password == confirm_password:
            if User.objects.filter(username = username).exists():
                messages.info(request, "Username already Exists!")
                return redirect('user_register')
            else:
                if User.objects.filter(email = email).exists():
                    messages.info(request, "Email already Exists!")
                    return redirect('user_register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    data = Customer(user=user, phone = phone)
                    data.save()

                    our_user = authenticate(username=username, password=password)
                    if our_user is not None:
                        login(request, user)
                        return redirect('/')
        else:
            messages.info(request, "Password and Confirm password Mismatch!")  
            return redirect('user_register')          
    return render(request, 'accountsapp/register.html')

def user_logout(request):
    logout(request)
    return redirect('/')