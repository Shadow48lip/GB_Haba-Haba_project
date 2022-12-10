from django import forms
from django.core.exceptions import ValidationError

from .models import HabaUser


class EditUserForm(forms.ModelForm):
    """Изменение своих данных пользователем."""

    password2 = forms.CharField(max_length=128, label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' '})
                                )

    class Meta:

        model = HabaUser
        # fields = '__all__'
        fields = ['username', 'email', 'first_name', 'gender', 'last_name', 'age', 'about', 'password', 'password2']
        # стили оформления и атрибуты каждого поля формы можно описать тут
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'cols': 60, 'rows': 5}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ' '}),
        }

    def clean_first_name(self):
        """Пример валидатора по полю first_name"""
        first_name = self.cleaned_data['first_name']
        if len(first_name) > 100:
            raise ValidationError('Длина превышает 100 символов')

        return first_name

    def clean_password(self):
        password
