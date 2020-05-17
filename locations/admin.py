from django.contrib import admin

from .models import Location, Type

# Register admin dashboard for Type & Location
class LocationAdmin(admin.ModelAdmin):
    model = Location
    search_fields = ['name']

admin.site.register(Type)
admin.site.register(Location,LocationAdmin)
