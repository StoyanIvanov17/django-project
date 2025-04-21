from django.urls import path

from project.accounts import views

urlpatterns = [
    path('login/', views.SignInUserView.as_view(), name='login'),
    path('register/', views.SignUpUserView.as_view(), name='register'),
]