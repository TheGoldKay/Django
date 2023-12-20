from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "index.html")

def home(request):
    return HttpResponse(f"{str(request)} - > You're at the homepage: Got to /polls/")