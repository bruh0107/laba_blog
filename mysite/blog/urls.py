from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/delete/', views.delete_profile, name='delete_profile'),

    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),

path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
