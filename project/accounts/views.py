from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, logout, get_user_model

from project.accounts.forms import UserCreationForm, CustomAuthenticationForm
from project.accounts.models import Customer, CustomUser

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
        user = self.object

        Customer.objects.create(
            user=user,
            first_name='',
            last_name='',
            phone_number='',
            country='',
            date_of_birth=user.date_of_birth,
        )

        login(self.request, user)
        return redirect('homepage')

    def form_invalid(self, form):
        print("form_invalid called — errors:", form.errors)
        return super().form_invalid(form)


class CheckEmailView(views.View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        if email:
            if UserModel.objects.filter(email=email).exists():
                return JsonResponse({'exists': True})
            else:
                return JsonResponse({'exists': False})
        return JsonResponse({'error': 'Email not provided'}, status=400)


class AccountDetailsView(views.DetailView):
    model = Customer
    template_name = 'accounts/profile_page.html'

    def get_object(self, queryset=None):
        customer, created = Customer.objects.get_or_create(
            user=self.request.user,
            defaults={
                'first_name': '',
                'last_name': '',
                'phone_number': '',
                'country': '',
                'date_of_birth': self.request.user.date_of_birth,
            }
        )
        return customer


@login_required
def logout_user(request):

    logout(request)
    return redirect('homepage')
