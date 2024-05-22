from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import OTPToken
from django.contrib.auth import get_user_model
User=get_user_model()
from django.core.mail import send_mail
from django.utils import timezone
from .forms import LoginForm,RegisterForm
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
    return render(request, "register.html",{"form":form})

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
    return render(request, "login.html", {"form":form})
        

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
            else:
                messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
                return redirect("verify-email", email=user.email)
        
        context = {}
        return render(request, "token.html", context)

            
def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OTPToken.objects.create(user=user, expire=timezone.now() + timezone.timedelta(minutes=5))
            
            subject="Email Verification"
            message = f"""
                                Hi {user.email}, here is your OTP {otp.otp_code} 
                                it expires in 5 minute, use the url below to redirect back to the website
                                http://127.0.0.1:8000/verify-email/{user.email}
                                
                                """
            sender = ""
            receiver = [user.email, ]
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email",email=user.email)
        
        else:
            messages.warning(request, "This email is not registered")
            return redirect("resend-otp")
    context = {}
    return render(request, "resend.html", context)

def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")