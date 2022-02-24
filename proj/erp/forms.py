from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import *
# from hrm.models import Employee


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        # fields = '__all__'
        fields = ['username', 'first_name',
                  'last_name', 'email', 'sex', 'department']

        help_texts = {
            'username': None,
            'password1': None,
        }


class UpdateInfoForm(forms.ModelForm):

    class Meta:
        model = User

        fields = ['username', 'first_name', 'last_name', 'email', ]

        help_texts = {
            'username': None,
            'password1': None,
        }
