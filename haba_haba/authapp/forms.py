from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from userapp.models import HabaUser


class UserRegisterForm(UserCreationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'id_username_r',
                'placeholder': 'Username',
                "autofocus": True,
            }
        )
    )

    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'id_password1',
                'placeholder': 'Password',
                "autocomplete": "new-password"
            }
        ),
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'id_password2',
                'placeholder': 'Password',
                "autocomplete": "new-password"
            }
        ),
        strip=False,
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'id_email',
                'placeholder': 'Email',
            },
        ),
    )

    check = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'id_check',
                'placeholder': 'Activating',
            },
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = HabaUser
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'check',
        )


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'id_username_l',
                'placeholder': 'Username',
                "autofocus": True,
            }
        )
    )

    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'id_password',
                'placeholder': 'Password',
                'autocomplete': 'current-password',
            }
        ),
    )


