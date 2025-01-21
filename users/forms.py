from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from main.models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        # model = Profile
        fields = ['username', 'email', 'password1', 'password2']