from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import OtpToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from .forms import LoginForm, RegisterForm
from django.conf import settings
from django.core.mail import send_mail

User = get_user_model()

def index(request):
    context = {
        "title": "Home Page"
    }
    return render(request, "index.html", context)

def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! An OTP was sent to your Email")
            return redirect("verify-email", username=request.POST['username'])
    context = {"form": form}
    return render(request, "register.html", context)

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def verify_email(request, username):
    user = User.objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    if request.method == 'POST':
        if user_otp.otp_code == request.POST['otp_code']:
            if user_otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, "Account activated successfully! You can log in.")
                return redirect("login")
            else:
                messages.warning(request, "The OTP has expired, please request a new OTP.")
                return redirect("verify-email", username=user.username)
        else:
            messages.warning(request, "Invalid OTP entered, please enter a valid OTP.")
            return redirect("verify-email", username=user.username)
    
    context = {}
    return render(request, "token.html", context)

def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        
        if User.objects.filter(email=user_email).exists():
            user = User.objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            subject = "Email Verification"
            message = f"""
                        Hi {user.username}, here is your OTP {otp.otp_code}. 
                        It expires in 5 minutes. Use the URL below to verify your email:
                        http://127.0.0.1:8000/verify-email/{user.username}
                      """
            sender = settings.DEFAULT_FROM_EMAIL
            receiver = [user.email]
        
            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )
            
            messages.success(request, "A new OTP has been sent to your email address.")
            return redirect("verify-email", username=user.username)
        else:
            messages.warning(request, "This email does not exist in our database.")
            return redirect("resend-otp")
    context = {}
    return render(request, "resend.html", context)

def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")