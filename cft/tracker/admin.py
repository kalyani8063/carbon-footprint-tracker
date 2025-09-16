from django.contrib import admin
from .models import Profile, Activity, Emission, Community, Challenge

# Register your models here to make them accessible in the Django admin panel.

# This will allow you to see and edit Profile objects in the admin.
admin.site.register(Profile)

# This will allow you to see and edit Activity objects.
admin.site.register(Activity)

# This will allow you to see and edit Emission objects.
admin.site.register(Emission)


admin.site.register(Community)
admin.site.register(Challenge)