from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import HabaUser


class EditUserForm(forms.ModelForm):
    """Изменение своих данных пользователем."""

    password1 = forms.CharField(
        max_length=128,
        label='Новый пароль',
        required=False,
        validators=[validate_password],
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': ' '
            }
        )
    )
    password2 = forms.CharField(
        max_length=128,
        label='Подтверждение пароля',
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'id_password',
                'placeholder': 'Password',
            }
        )
    )

    class Meta:
        model = HabaUser
        # fields = '__all__'
        fields = ['username', 'email', 'first_name', 'gender', 'last_name', 'age', 'about', 'password1', 'password2']
        # стили оформления и атрибуты каждого поля формы можно описать тут
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'gender': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'age': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'about': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
            # 'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' '}),
        }

    # def clean_password1(self):
    #     """Пример валидатора по полю password1"""
    #     password1 = self.cleaned_data['password1']
    #     if len(password1) < 5:
    #         raise ValidationError('Длина пароля слишком маленькая')
    #
    #     return password1
