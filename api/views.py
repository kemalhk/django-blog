from django.shortcuts import render, redirect, get_object_or_404

# from django.http import HttpResponse
# from rest_framework.response import Response
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# from rest_framework.authtoken.models import Token
# from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .forms import UserRegistrationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

# from django.contrib.auth.forms import AuthenticationForm
from .models import Category, Comment, Post


# Create your views here.


def home(request):
    latest_posts = Post.objects.order_by("-created_at")[:12]
    context = {"latest_posts": latest_posts}
    return render(request, "home.html", context)


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
            """token, created = Token.objects.get_or_create(user=user)"""
            login(request, user)

            return redirect("home")
        else:
            error_message = "Kullanıcı adı veya şifre yanlış."
            return render(request, "login.html", locals())
    else:
        return render(request, "login.html", locals())


def logoutUser(request):
    # Kullanıcının tokenı varsa tokenı sil
    """if request.user.is_authenticated:
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
    except Token.DoesNotExist:
        pass"""
    logout(request)
    return redirect("home")


def haber(request):
    haber_category = Category.objects.filter(category_title="Haber").first()
    print(haber_category)
    haber_posts = Post.objects.filter(category_title=haber_category)
    print(haber_posts)
    return render(request, "haber.html", locals())


def makale(request):
    makale_category = Category.objects.filter(category_title="Makale").first()
    print(makale_category)
    makale_posts = Post.objects.filter(category_title=makale_category)
    print(makale_posts)

    return render(request, "makale.html", locals())


def tavsiyeler(request):
    tavsiyeler_category = Category.objects.filter(category_title="Tavsiyeler").first()
    print(tavsiyeler_category)
    tavsiyeler_posts = Post.objects.filter(category_title=tavsiyeler_category)
    print(tavsiyeler_posts)
    return render(request, "tavsiyeler.html", locals())


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "post_detail.html", {"post": post})
