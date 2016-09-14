# -*- coding: UTF-8 -*-
from django import forms
from problems.models import UserProfile
from django.contrib.auth.models import User

my_default_errors = {
    'required': 'Tolts ki plz.',
    'invalid': 'Rendesen toltsd ki plz'
} # Igy lehet felulirni a default error-t

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'password' )
        
class UserProfileForm(forms.ModelForm):
    #has_notification = forms.BooleanField
    class Meta:
        model = UserProfile
        fields = ('local_picture',)

