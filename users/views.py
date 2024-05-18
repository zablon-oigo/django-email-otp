from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import OTPToken
from django.contrib.auth import get_user_model
User=get_user_model()
from django.utils import timezone
def index(request):
    context={
        "title":"Home Page"
    }
    return render(request, "index.html", context)

def register_user(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=True
            user.save()
            messages.success(request, "Account created successfully,Please check your email")
            return redirect("verify-email")
    
    else:
        form=RegisterForm()
    return render(request, "users/register.html",{"form":form})

def login_user(request):
    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.clean_data["email"]
            password=form.clean_date["password"]
            user=authenticate(request,email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect("home")
    
    else:
        form=LoginForm()
    return render(request, "users/login.html", {"form":form})
        

def verify_email(request,email):
        user = User.objects.get(email=email)
        user_otp =OTPToken.objects.filter(user=user).last()

        if request.method == "POST":
            if user_otp.otp_code == request.POST['otp_code']:
                if user_otp.otp_expires_at > timezone.now():
                    user.is_active=True
                    user.save()
                    messages.success(request, "Account activated successfully!!")
                    return redirect("login")
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify-email", email=user.email)
            

