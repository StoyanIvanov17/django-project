from django.views import generic as views

from project.accounts.forms import (
    UserCreationForm,
    CustomAuthenticationForm,
)


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

        context['sections'] = [
            {
                'title': 'Tennis Collection',
                'description': 'Lightweight, flexible pieces built for the court.',
                'button_text': 'Shop Tennis',
                'button_url': '/products/?category=tennis',
                'image': 'images/tennis_homepage.jpg',
            },
            {
                'title': 'Ski Collection',
                'description': 'Lightweight, flexible pieces built for the snow course.',
                'button_text': 'Shop Ski',
                'button_url': '/products/?category=ski',
                'image': 'images/ski_homepage.jpg',
            },
            {
                'title': 'Golf Collection',
                'description': 'Performance apparel designed for every round.',
                'button_text': 'Shop Golf',
                'button_url': '/products/?category=golf',
                'image': 'images/golf_homepage_2.jpg',
            },
            {
                'title': 'Everyday Collection',
                'description': 'Versatile styles for life beyond sport.',
                'button_text': 'Shop Everyday',
                'button_url': '/products/?category=everyday',
                'image': 'images/everyday_homepage.jpg',
            },
            {
                'title': 'Travel Collection',
                'description': 'Versatile styles for life beyond sport.',
                'button_text': 'Shop Everyday',
                'button_url': '/products/?category=travel',
                'image': 'images/travel_homepage.jpg',
            },
        ]

        return context
