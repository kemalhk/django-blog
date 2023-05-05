from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.response import Response
from django.template import loader
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .forms import UserRegistrationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def home(request):
    template = loader.get_template("home.html")
    return HttpResponse(template.render())


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("home")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error_message = "Kullanıcı adı veya şifre yanlış."
            return render(request, "login.html", {"error_message": error_message})
    else:
        return render(request, "login.html")
