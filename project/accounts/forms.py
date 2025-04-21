from django.contrib.auth import forms as auth_forms, get_user_model
from django.core.exceptions import ValidationError

UserModel = get_user_model()


class UserCreationForm(auth_forms.UserCreationForm):
    MIN_PASSWORD_LENGTH = 8
    usable_password = None
    user = None

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        if len(password1) < self.MIN_PASSWORD_LENGTH:
            raise ValidationError(
                f"Password must be at least {self.MIN_PASSWORD_LENGTH} characters long."
            )

        if not any(char.isalpha() for char in password1):
            raise ValidationError("Password must contain at least one letter.")

        return password2