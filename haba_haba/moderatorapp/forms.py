from django import forms


class ComplainAction(forms.Form):
    """Форма реакции на жалобу"""
    reason = forms.CharField(
        max_length=255,
        label="Причина принятия решения",
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
            })
        )

    user_block_days = forms.IntegerField(
        label="Заблокировать пользователя (дней)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            })
        )

    action_hide = forms.BooleanField(
        label="Снять с публикации",
        required=False,
        # widget = forms.CheckboxInput(
        #     attrs={
        #         'class': 'form-control',
        #     })
        )

