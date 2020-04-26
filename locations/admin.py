from django.contrib import admin

from .models import Location, Type

# Register admin dashboard for Type & Location
admin.site.register(Type)
admin.site.register(Location)
