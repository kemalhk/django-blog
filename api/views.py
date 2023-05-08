from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.response import Response
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .forms import UserRegistrationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from .models import Category, Comment, Post


# Create your views here.


def home(request):
    return render(request, "home.html")


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("home")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        """ username = form.cleaned_data["username"]
        password = form.cleaned_data["password"] """
        user = authenticate(request, username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)

            return redirect("home")
        else:
            error_message = "Kullanıcı adı veya şifre yanlış."
            return render(request, "login.html", locals())
    else:
        return render(request, "login.html", locals())


def logoutUser(request):
    # Kullanıcının tokenı varsa, tokenı silin
    if request.user.is_authenticated:
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass
    logout(request)
    return redirect("home")
