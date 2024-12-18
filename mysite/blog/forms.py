from django import forms
from django.core.exceptions import ValidationError

from .models import CustomUser, Post, Comment

class CustomUserCreatingForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=150)
    email = forms.EmailField(label='E-mail', max_length=254)
    bio = forms.CharField(label='Описание', widget=forms.Textarea)
    avatar = forms.FileField(label='Загрузите свой аватар', widget=forms.FileInput, required=True)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердить пароль", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Такой username уже занят')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Такой email уже занят')
        return email

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Пароли не совпадают')
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if self.cleaned_data.get('image'):
            user.avatar = self.cleaned_data.get('image')
        if commit:
            user.save()
            return user

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'avatar')

class CustomUserChangeForm(forms.ModelForm):
    avatar = forms.FileField(label='Фото профиля', widget=forms.FileInput, required=False)
    email = forms.EmailField(label='Email', max_length=254, required=True)
    bio = forms.CharField(label='Описание заявки', widget=forms.Textarea)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Этот email уже используется.')
        return email

    class Meta:
        model = CustomUser
        fields = ['email', 'avatar', 'bio']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class LikeForm(forms.Form):
    pass