from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
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
        form=LoginForm()
        if form.is_valid():
            email=form.clean_data["email"]
            password=form.clean_date["password"]
            user=authenticate(request,email=email, password=password)
        
