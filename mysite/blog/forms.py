from django import forms
from .models import CustomUser, Post, Comment
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreatingForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'avatar', 'bio', 'password1', 'password2']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'avatar', 'bio']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']