from django.contrib import admin

from .models import Page

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    model = Page
    filter_horizontal = ('categories',)

admin.site.register(Page, PageAdmin )
