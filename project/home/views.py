from django.shortcuts import render
from django.views import generic as views


class HomeView(views.TemplateView):
    template_name = 'home/homepage.html'
