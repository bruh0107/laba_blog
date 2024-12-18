from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Post, Comment
from .forms import CustomUserChangeForm, PostForm, CommentForm, CustomUserCreatingForm
from django.contrib import messages

def home(request):
    posts = Post.objects.all().order_by('-created_at')[:20]
    return render(request, "blog/home.html", {"posts": posts})


@login_required
def edit_profile(request, username):
    # Получаем пользователя по username
    user = get_object_or_404(CustomUser, username=username)

    # Проверяем, что это текущий вошедший пользователь
    if request.user != user:
        return redirect('blog:profile', username=request.user.username)

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=user.username)
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, "blog/edit_profile.html", {"form": form, "user": user})

def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    posts = user.posts.all()
    return render(request, "blog/profile.html", {"user_profile": user, "posts": posts})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "blog/create_post.html", {"form": form})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect("blog:home")
    return redirect("blog:home")

def register(request):
    if request.method == "POST":
        form = CustomUserCreatingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш аккаунт был успешно создан! Теперь вы можете войти.")
            return redirect('blog:login')
    else:
        form = CustomUserCreatingForm()
    return render(request, 'blog/register.html', {'form': form})

