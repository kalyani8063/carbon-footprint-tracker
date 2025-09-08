# tracker/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model, decorators
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
# Import the Profile model
from .models import Profile
import json
from datetime import date, timedelta
import random

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name}! Your account has been created.")
            return redirect('tracker-home')
    else:
        form = UserRegisterForm()
    return render(request, 'tracker/register.html', {'form': form})

def home(request):
    return render(request, 'tracker/home.html')

@decorators.login_required
def myprofile(request):
    # --- FIX: Get or create the profile for the current user ---
    # This ensures that even users created before the signals were in place will get a profile.
    Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('myprofile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # --- Dashboard Data (remains the same) ---
    total_footprint_this_month = 450.7
    ranking_data = {
        'city': {'rank': 12, 'total': 150},
        'state': {'rank': 89, 'total': 1200},
        'country': {'rank': 1520, 'total': 25000}
    }
    category_data = {
        'labels': ["Transportation", "Energy", "Food", "Purchases"],
        'data': [150.2, 180.5, 90.0, 30.0],
    }
    trends_data = {
        'labels': ["March", "April", "May", "June", "July", "August"],
        'data': [510, 480, 495, 460, 475, 450],
    }
    carbon_budget = {
        'limit': 500,
        'used': total_footprint_this_month,
        'percentage': round((total_footprint_this_month / 500) * 100)
    }
    actionable_insights = [
        {"text": "Your energy consumption is the biggest contributor.", "icon": "fas fa-lightbulb"},
        {"text": "Switching one car trip to public transit could save ~15kg CO₂e this month.", "icon": "fas fa-bus"},
        {"text": "You're 10% below your monthly carbon budget. Keep it up!", "icon": "fas fa-bullseye"},
    ]
    today = date.today()
    active_days_set = set()
    for i in range(120):
        if random.random() < 0.5:
            active_day = today - timedelta(days=i)
            active_days_set.add(active_day.strftime("%Y-%m-%d"))
    
    streak_data_for_chart = {
        "total_active": len(active_days_set),
        "max_streak": 8,
        "active_days": sorted(list(active_days_set))
    }

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'total_footprint_this_month': total_footprint_this_month,
        'ranking_data': ranking_data,
        'category_data_json': json.dumps(category_data),
        'trends_data_json': json.dumps(trends_data),
        'streak_data_json': json.dumps(streak_data_for_chart),
        'carbon_budget': carbon_budget,
        'actionable_insights': actionable_insights,
    }
    return render(request, 'tracker/myprofile.html', context)

