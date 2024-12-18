from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import CustomUser, Post, Comment
from .forms import CustomUserChangeForm, PostForm, CommentForm, CustomUserCreatingForm
from django.contrib import messages

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    comment_count = [
        {
            "post": post,
            'comments_count': post.comments.count()
        }
        for post in page_obj.object_list
    ]

    return render(request, "blog/home.html", {
        "posts": posts,
        "page_obj": page_obj,
        "comment_count": comment_count
    })

@login_required
def edit_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
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
            return redirect("blog:home")
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

@login_required
def delete_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    if request.user == user:
        user.posts.update(author=None)
        user.posts.update(author_name="Удаленный пользователь")

        Comment.objects.filter(author=user).update(author=None)
        Comment.objects.filter(author=user).update(author_name="Удалённый пользователь")

        user.delete()
        messages.success(request, 'Ваш профиль удален.')
        return redirect('blog:home')
    messages.error(request, 'вы не можете удалить чужой профиль')
    return redirect('blog:home')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user not in post.likes.all():
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)

    return redirect('blog:home')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш пост был успешно обновлен!")
            return redirect('blog:home')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {"form": form, "post": post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Ваш пост удален")
        return redirect("blog:home")
    return render(request, "blog/delete_post.html", {"post": post})
