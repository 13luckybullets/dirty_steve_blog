from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, EmailField
from .models import *


class SignUpForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class UpdateEmail(ModelForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']

