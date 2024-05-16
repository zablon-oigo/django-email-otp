from django.shortcuts import render

def index(request):
    context={
        "title":"Home Page"
    }
    return render(request, "index.html", context)
