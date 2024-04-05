from django.shortcuts import render
from solidsocial.util.model import get_own_id

def AboutView(request):
    return render(request, "about.html", {
        "current": "About", 
        })
