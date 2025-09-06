# tracker/context_processors.py

from datetime import date, timedelta
import random

def navbar_stats(request):
    """
    Provides global context for the navigation bar,
    making streak and achievement data available on every page.
    """
    # We only need to calculate this if the user is logged in.
    if request.user.is_authenticated:
        # Dummy data for achievements
        achievements = [
            {"name": "Monthly Champion", "description": "Footprint under 400kg for a month.", "icon": "fas fa-tree", "tier": "gold"},
            {"name": "Weekly Saver", "description": "Footprint under 100kg for a week.", "icon": "fas fa-leaf", "tier": "silver"},
            {"name": "Daily Green", "description": "Kept footprint under 15kg for a day.", "icon": "fas fa-seedling", "tier": "bronze"},
            {"name": "Eco-Starter", "description": "Logged your first activity.", "icon": "fas fa-award", "tier": "bronze"},
        ]

        # Dummy data for activity streaks
        today = date.today()
        active_days_set = set()
        for i in range(120):
            if random.random() < 0.5:
                active_day = today - timedelta(days=i)
                active_days_set.add(active_day.strftime("%Y-%m-%d"))

        streak_data = {
            "total_active": len(active_days_set),
            "max_streak": 8
        }
        
        return {
            'global_achievements': achievements,
            'global_streak_data': streak_data,
        }
    
    # If user is not logged in, return an empty dictionary
    return {}
