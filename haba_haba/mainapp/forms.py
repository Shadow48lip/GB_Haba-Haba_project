from django import forms
from .models import Post
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "выберите категорию"

    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['title', 'cat', 'photo', 'content', 'tags', 'is_published']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', }),
            'cat': forms.Select(attrs={'class': 'form-control', }),
            'photo': forms.FileInput(attrs={'class': 'form-control', }),
            'content': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '500',
                }}),
            # 'content': SummernoteInplaceWidget(),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control', }),
        }
