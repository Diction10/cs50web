from email.policy import default
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from erp.models import *
from .models import *


class editEmployeeInfo(forms.ModelForm):
    salary = forms.IntegerField(required=False)

    class Meta:
        model = User
        # exclude = ['user']
        # fields = '__all__'
        fields = ['first_name', 'last_name',
                  'email', 'department', 'salary', 'sex']
