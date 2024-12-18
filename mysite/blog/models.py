from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(max_length=150, verbose_name='Email', unique=True)
    password = models.CharField(max_length=150, verbose_name='Пароль')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'avatar']

    def __str__(self):
        return self.username

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Пост от {self.author.username} в {self.created_at}"


    def comments_count(self):
        return Comment.objects.filter(post=self).count()

    def like_count(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Комментарий оставлен {self.author.username} в {self.post}"
