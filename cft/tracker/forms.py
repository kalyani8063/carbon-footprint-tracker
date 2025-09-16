from django import forms
from .models import User, Profile, Challenge, Community
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, max_length=30)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'email',)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'location', 'carbon_budget_kg']

class ChallengeForm(forms.ModelForm):
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Challenge
        fields = ['community', 'title', 'description', 'goal', 'unit', 'reward_achievement', 'end_date']
        help_texts = {
            'reward_achievement': 'Optional. Select a badge to award upon completion.'
        }