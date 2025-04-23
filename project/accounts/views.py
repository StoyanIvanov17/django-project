from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, logout, get_user_model

from project.accounts.forms import UserCreationForm, CustomAuthenticationForm

UserModel = get_user_model()


class SignInUserView(auth_views.LoginView):
    template_name = 'accounts/auth_modal.html'
    redirect_authenticated_user = True
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            return reverse("homepage")

        return super().get_success_url()


class SignUpUserView(views.CreateView):
    template_name = 'accounts/auth_modal.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def get_success_url(self):
        return self.success_url


class CheckEmailView(views.View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        if email:
            if UserModel.objects.filter(email=email).exists():
                return JsonResponse({'exists': True})
            else:
                return JsonResponse({'exists': False})
        return JsonResponse({'error': 'Email not provided'}, status=400)


@login_required
def logout_user(request):

    logout(request)
    return redirect('homepage')
