# tracker/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

# View for handling user registration
def register(request):
    # Check if the form has been submitted (POST request)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # Validate the form
        if form.is_valid():
            form.save() # Save the new user to the database
            username = form.cleaned_data.get('username')
            # Display a success message
            messages.success(request, f'Account created for {username}! You can now log in.')
            # Redirect the user to the login page
            return redirect('login')
    else:
        # If it's a GET request, just display a blank form
        form = UserRegisterForm()
    return render(request, 'tracker/register.html', {'form': form})

# A simple view for the home page, which requires the user to be logged in
@login_required
def home(request):
    return render(request, 'tracker/home.html')

