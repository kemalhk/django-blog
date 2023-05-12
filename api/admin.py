from django.contrib import admin
from .models import UserProfile, Comment, Post, Category

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Category)
