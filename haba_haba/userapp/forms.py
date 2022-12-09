from django import forms
from .models import HabaUser


class EditUserForm(forms.ModelForm):
    """Изменение своих данных пользователем."""

    class Meta:
        model = HabaUser
        fields = '__all__'  # ['first_name', 'last_name']
        # стили оформления и атрибуты каждого поля формы можно описать тут
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-input'}),
        #     'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        # }

