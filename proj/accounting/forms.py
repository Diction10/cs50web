from email.policy import default
from django import forms
from accounting.models import *

from django.contrib.auth.models import User
from .models import Billing
from django.contrib.auth import get_user_model


User = get_user_model()


class BillingForm(forms.ModelForm):

    class Meta:
        model = Billing
        # fields = '__all__'

        fields = ['product', 'quantity', 'transaction_date']
