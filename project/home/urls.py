from django.urls import path

from project.home import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='homepage')
]