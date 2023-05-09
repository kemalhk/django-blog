from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}), required=True
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args: Any, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
