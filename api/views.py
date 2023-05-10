from django.shortcuts import render, redirect, get_object_or_404

# from django.http import HttpResponse
# from rest_framework.response import Response
from django.template import loader
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

# from rest_framework.authtoken.models import Token
# from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .forms import UserRegistrationForm, CommentForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Category, Comment, Post
from django.core.paginator import Paginator

# Create your views here.


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
            # kullanıcı yorum yapmak için giriş yaptıysa direkt bulunduğu sayfaya yönlendirme
            redirect_to = request.GET.get("next", "home")
            return redirect(redirect_to)

        else:
            error_message = "Kullanıcı adı veya şifre yanlış."
            return render(request, "login.html", locals())
    else:
        return render(request, "login.html", locals())


def user_change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("password")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", locals())


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


def home(request):
    # anasayfada listelenicek post sayısı
    # latest_posts = Post.objects.order_by("-created_at")[:12]
    # set up pagination
    p = Paginator(Post.objects.order_by("-created_at"), 1)
    page = request.GET.get("page")
    homepage_list = p.get_page(page)
    nums = range(1, homepage_list.paginator.num_pages + 1)
    return render(request, "home.html", locals())


def haber(request):
    haber_category = Category.objects.filter(category_title="Haber").first()
    # set up pagination
    p = Paginator(
        Post.objects.filter(category_title=haber_category).order_by("-created_at"), 1
    )
    page = request.GET.get("page")
    haber_list = p.get_page(page)
    nums = range(1, haber_list.paginator.num_pages + 1)
    return render(request, "haber.html", locals())


def makale(request):
    makale_category = Category.objects.filter(category_title="Makale").first()
    p = Paginator(
        Post.objects.filter(category_title=makale_category).order_by("-created_at"), 1
    )
    page = request.GET.get("page")
    makale_posts = p.get_page(page)
    nums = range(1, makale_posts.paginator.num_pages + 1)
    return render(request, "makale.html", locals())


def tavsiyeler(request):
    tavsiyeler_category = Category.objects.filter(category_title="Tavsiyeler").first()
    p = Paginator(
        Post.objects.filter(category_title=tavsiyeler_category).order_by("-created_at"),
        1,
    )
    page = request.GET.get("page")
    tavsiyeler_posts = p.get_page(page)
    nums = range(1, tavsiyeler_posts.paginator.num_pages + 1)
    return render(request, "tavsiyeler.html", locals())


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # set up pagination
    p = Paginator(post.comments.order_by("-created_at"), 1)
    page = request.GET.get("page")
    post_detail_comments_list = p.get_page(page)
    nums = range(1, post_detail_comments_list.paginator.num_pages + 1)

    return render(request, "post_detail.html", locals())


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.content = form.cleaned_data["yorum"]  # burada değişiklik yapıldı
            comment.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = CommentForm()

    # kullanıcı giriş yapmamış ise, login sayfasına yönlendir
    if not request.user.is_authenticated:
        return redirect(
            reverse_lazy("login")
            + f"?next={reverse_lazy('add_comment', args=[post.pk])}"
        )
    return render(request, "post_detail.html", {"form": form, "post": post})


@login_required
def profil_comments(request):
    user = request.user
    # kullanıcının yorumlarının listlenmesi
    # comments = Comment.objects.filter(author=user).order_by("-created_at")
    comments = Comment.objects.filter(author=user).order_by("-created_at")

    # set up pagination
    p = Paginator(Comment.objects.filter(author=user).order_by("-created_at"), 1)
    page = request.GET.get("page")
    comments_list = p.get_page(page)
    nums = "a" * comments_list.paginator.num_pages
    return render(request, "profil.html", locals())


@login_required
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.content = form.cleaned_data["yorum"]
            comment.author = request.user
            comment.post = get_object_or_404(Post, pk=comment.post.pk)
            comment.save()
            return redirect("comments")
    return redirect("comments")


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Yorum başarıyla silindi.")
        return redirect("comments")

    context = {"comment": comment}
    return render(request, "profil.html", context)
