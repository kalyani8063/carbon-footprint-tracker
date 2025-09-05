# tracker/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from .forms import UserRegisterForm
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
            messages.success(request, f"Account created successfully for {user.username}!")
            return redirect('tracker-home')
    else:
        form = UserRegisterForm()
    return render(request, 'tracker/register.html', {'form': form})

def home(request):
    total_users = User.objects.count()
    total_footprint_this_month = 450.7

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
    
    comparison_data = {
        'personal': total_footprint_this_month,
        'national_average': 850,
    }
    
    actionable_insights = [
        {"text": "Your energy consumption is the biggest contributor. Consider switching to LED bulbs.", "icon": "fas fa-lightbulb"},
        {"text": "Switching one car trip to public transit could save ~15kg CO₂e this month.", "icon": "fas fa-bus"},
        {"text": "You're 10% below your monthly carbon budget. Keep it up!", "icon": "fas fa-bullseye"},
    ]
    
    achievements = [
        {"name": "Monthly Champion", "description": "Footprint under 400kg for a month.", "icon": "fas fa-tree", "tier": "gold"},
        {"name": "Weekly Saver", "description": "Footprint under 100kg for a week.", "icon": "fas fa-leaf", "tier": "silver"},
        {"name": "Daily Green", "description": "Kept footprint under 15kg for a day.", "icon": "fas fa-seedling", "tier": "bronze"},
        {"name": "Eco-Starter", "description": "Logged your first activity.", "icon": "fas fa-award", "tier": "bronze"},
    ]
    
    today = date.today()
    # THIS LINE WAS MISSING AND IS NOW FIXED
    active_days_set = set()
    for i in range(120):
        if random.random() < 0.5:
            active_day = today - timedelta(days=i)
            active_days_set.add(active_day.strftime("%Y-%m-%d"))
    
    streak_data = {
        "total_active": len(active_days_set),
        "max_streak": 8,
        "active_days": sorted(list(active_days_set))
    }

    context = {
        'total_users': total_users,
        'total_footprint_this_month': total_footprint_this_month,
        'category_data_json': json.dumps(category_data),
        'trends_data_json': json.dumps(trends_data),
        'streak_data_json': json.dumps(streak_data),
        'carbon_budget': carbon_budget,
        'comparison_data': comparison_data,
        'actionable_insights': actionable_insights,
        'achievements': achievements,
        'streak_data': streak_data,
    }
    return render(request, 'tracker/home.html', context)
