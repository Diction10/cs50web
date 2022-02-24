from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import *


class addInventory(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['user']
        fields = '__all__'
