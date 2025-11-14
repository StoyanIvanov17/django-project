from django.urls import path

from project.accounts import views

urlpatterns = [
    path('login/', views.SignInUserView.as_view(), name='account-login'),
    path('register/', views.SignUpUserView.as_view(), name='account-register'),
    path('logout/', views.logout_user, name='account-logout'),
    path('account/', views.AccountDetailsView.as_view(), name='account-details'),

    path('check-email/', views.CheckEmailView.as_view(), name='check-email'),
]
