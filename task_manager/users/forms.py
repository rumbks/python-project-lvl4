from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):
    error_messages = {
        "passwords_dont_match": _("Two passwords should match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(),
        help_text=_("Your password should be at least 3 symbols long."),
    )
    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput(),
        help_text=_("Re-enter your password again, please."),
    )

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "username",
        ]
        localized_fields = [
            "first_name",
            "last_name",
            "username",
        ]
        labels = {
            "first_name": _("First name"),
            "last_name": _("Last name"),
            "username": _("Username"),
        }
        help_texts = {
            "username": _(
                "Required. Char limit 150. Allowed symbols "
                "are letters, digits and @/./+/-/_."
            ),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["passwords_dont_match"],
                code="passwords_dont_match",
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user
