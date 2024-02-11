from django.contrib import admin
from .models import About


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    """
    Class for About Admin model
    """
    list_display = ('title', 'text', 'image')
