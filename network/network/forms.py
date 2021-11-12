from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import *


class NewPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['post_content']

        # Override the name of the field
        labels = {'post_content': ('New Post'),}
        widgets = {'summary': forms.Textarea(attrs={'rows':0, 'cols':0}),}



