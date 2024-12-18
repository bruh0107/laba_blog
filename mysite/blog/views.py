from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Post, Comment
from .forms import CustomUserChangeForm


def home(request):
    posts = Post.objects.all().order_by('-created_at')[:20]
    return render(request, "blog/home.html", {"posts": posts})

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, "blog/edit_profile.html", {"form": form})

def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    posts = user.posts.all()
    return render(request, "blog/profile.html")