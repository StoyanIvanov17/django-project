from django.views import generic as views

from project.accounts.forms import (
    UserCreationForm,
    CustomAuthenticationForm,
)
from project.products.models import Activity


class HomeView(views.TemplateView):
    template_name = 'home/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['register_form'] = UserCreationForm()
        context['login_form'] = CustomAuthenticationForm()

        context['auth_email'] = (
            self.request.session.get('auth_email', '')
        )

        context['open_register_modal'] = (
            self.request.session.pop('open_register_modal', False)
        )

        context['register_errors'] = (
            self.request.session.pop('register_errors', None)
        )

        context['open_login_modal'] = (
            self.request.session.pop('open_login_modal', False)
        )

        context['login_errors'] = (
            self.request.session.pop('login_errors', None)
        )

        context['login_non_field_errors'] = (
            self.request.session.pop('login_non_field_errors', None)
        )

        context['sections'] = (
            Activity.objects
            .filter(featured_on_homepage=True)
            .order_by('homepage_order')
        )

        return context
