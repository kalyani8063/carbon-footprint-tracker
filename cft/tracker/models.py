from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Activity(models.Model):
    ACTIVITY_CATEGORIES = [
        ('transport', 'Transportation'),
        ('energy', 'Home Energy'),
        ('food', 'Food & Diet'),
        ('consumption', 'Consumption'),
        ('waste', 'Waste'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=ACTIVITY_CATEGORIES)
    description = models.CharField(max_length=255)
    value = models.FloatField()
    unit = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.description} on {self.timestamp.strftime('%Y-%m-%d')}"

class Emission(models.Model):
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE)
    co2_equivalent_kg = models.FloatField()
    calculation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emission for {self.activity.description}: {self.co2_equivalent_kg} kg CO2e"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

