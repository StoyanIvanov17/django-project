import uuid
from django.contrib.auth import mixins as auth_mixin

from asgiref.sync import sync_to_async
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, logout, get_user_model
from django.shortcuts import render

from project.accounts.forms import UserCreationForm


class SignInUserView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):

        user = self.request.user
        if user.is_authenticated and hasattr(user, 'customer'):
            return reverse("homepage")

        return super().get_success_url()


class SignUpUserView(views.CreateView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('homepage')

    def get_success_url(self):
        return self.success_url


def signout_user(request):
    logout(request)
    return redirect('home page')