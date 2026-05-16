from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, logout, get_user_model

from project.accounts.forms import UserCreationForm, CustomAuthenticationForm
from project.accounts.models import Customer

UserModel = get_user_model()


class SignInUserView(auth_views.LoginView):
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect("homepage")

    def form_invalid(self, form):
        self.request.session['open_login_modal'] = True
        self.request.session['login_errors'] = form.errors.get_json_data()
        self.request.session['login_non_field_errors'] = form.non_field_errors()

        return redirect("homepage")


class SignUpUserView(views.CreateView):
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()

        Customer.objects.create(
            user=user,
            first_name='',
            last_name='',
            phone_number='',
            country='',
            date_of_birth=form.cleaned_data['date_of_birth'],
        )

        login(self.request, user)

        return redirect('homepage')

    def form_invalid(self, form):
        self.request.session['open_register_modal'] = True
        self.request.session['register_errors'] = form.errors.get_json_data()

        return redirect('homepage')


class CheckEmailView(views.View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        if email:

            request.session['auth_email'] = email

            if UserModel.objects.filter(email=email).exists():
                return JsonResponse({'exists': True})
            else:
                return JsonResponse({'exists': False})

        return JsonResponse(
            {'error': 'Email not provided'},
            status=400
        )


class AccountDetailsView(views.DetailView):
    model = Customer
    template_name = 'accounts/profile_page.html'

    def get_object(self, queryset=None):
        customer, created = Customer.objects.get_or_create(
            user=self.request.user,
        )
        return customer


@login_required
def logout_user(request):
    logout(request)
    return redirect('homepage')