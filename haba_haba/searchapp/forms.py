from django import forms

ORDER_CHOICES = (
    ("-time_create", "по времени"),
    ("-total_views", "по популярности"),

)


class SearchForm(forms.Form):
    """Форма реакции на жалобу"""
    q = forms.CharField(
        max_length=50,
        label="Что ищем",
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'строка поиска',
            })
    )

    order_by = forms.ChoiceField(
        label="Фильтр",
        choices=ORDER_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            })
    )

