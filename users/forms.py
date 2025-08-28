from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from mailings.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserForm(StyleFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ['first_name', "last_name", 'avatar', 'phone_number', 'country',]
