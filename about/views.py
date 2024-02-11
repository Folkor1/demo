from django.shortcuts import render
from django.views import generic
from .models import About


class AboutView(generic.ListView):
    """
    Render about page
    """
    model = About
    template_name = "about.html"
