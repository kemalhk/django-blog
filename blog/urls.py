"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home),
    path("home/", views.home, name="home"),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("profil_comments/", views.profil_comments, name="comments"),
    path("password/", views.user_change_password, name="password"),
    path("haber/", views.haber, name="haber"),
    path("makale/", views.makale, name="makale"),
    path("tavsiyeler/", views.tavsiyeler, name="tavsiyeler"),
    path("post_detail/<int:pk>/", views.post_detail, name="post_detail"),
    path(
        "post_detail/<int:pk>/add_comment/",
        views.add_comment_to_post,
        name="add_comment",
    ),
    path("comment/<int:pk>/update/", views.comment_update, name="comment_update"),
    path("comment/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
]
# path("register/", views.register, name="register"),
