from django.shortcuts import render
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
