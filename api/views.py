from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.response import Response
from django.template import loader
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect


# Create your views here.
def home(request):
    template = loader.get_template("home.html")
    return HttpResponse(template.render())


def register(request):
    template = loader.get_template("register.html")
    return HttpResponse(template.render())


@csrf_protect
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "login.html",
                {"error_message": "Invalid username or password."},
            )

    elif request.method == "GET":
        template = loader.get_template("login.html")
        return HttpResponse(template.render())


def login(request):
    template = loader.get_template("login.html")
    return HttpResponse(template.render())
