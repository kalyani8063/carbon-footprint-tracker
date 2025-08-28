# tracker/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# This form inherits from Django's UserCreationForm
# We are adding an email field which is required for registration
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        # Define the fields that will be displayed in the form
        fields = ['username', 'email']

