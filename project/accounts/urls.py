from django.urls import path

from project.accounts import views

urlpatterns = [
    path('login/', views.SignInUserView.as_view(), name='login'),
    path('register/', views.SignUpUserView.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('check-email/', views.CheckEmailView.as_view(), name='check_email'),
]
