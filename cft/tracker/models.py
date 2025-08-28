# tracker/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Model to extend the built-in User model with extra profile information
class UserProfile(models.Model):
    # This creates a one-to-one link with Django's existing User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # We can add more fields here later, like a profile picture or location

    def __str__(self):
        return self.user.username

# Model for different types of communities (e.g., University, Company)
class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name='communities')

    def __str__(self):
        return self.name

# Model to store each individual activity logged by a user
class Activity(models.Model):
    # Define choices for the category of the activity
    ACTIVITY_CATEGORIES = [
        ('transport', 'Transportation'),
        ('energy', 'Home Energy'),
        ('food', 'Food & Diet'),
        ('consumption', 'Consumption'),
        ('waste', 'Waste'),
    ]

    # Link the activity to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=ACTIVITY_CATEGORIES)
    description = models.CharField(max_length=255) # e.g., "Drove to work", "Ate a beef burger"
    value = models.FloatField() # e.g., distance in km, energy in kWh, quantity
    unit = models.CharField(max_length=50) # e.g., "km", "kWh", "servings"
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.description} on {self.timestamp.strftime('%Y-%m-%d')}"

# Model to store the calculated carbon emission for each activity
class Emission(models.Model):
    # Link this emission calculation to a specific activity
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE)
    # The calculated carbon footprint in kilograms of CO2 equivalent
    co2_equivalent_kg = models.FloatField()
    calculation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emission for {self.activity.description}: {self.co2_equivalent_kg} kg CO2e"

