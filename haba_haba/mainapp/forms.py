from django import forms
from .models import Post, Tag
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Выберите категорию"

    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['title', 'cat', 'photo', 'content', 'tags', 'is_published']

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'id_title',
                    'placeholder': 'Title',
                    "autofocus": True,
                }
            ),
            'cat': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'id_cat',
                }
            ),
            'photo': forms.FileInput(
                attrs={
                    'class': 'form-control form-control-lg h-floating',
                    'id': 'id_photo',
                }
            ),
            'content': SummernoteWidget(
                attrs={
                    'class': 'form-control',
                    'data-id': 'id_content',
                    'summernote': {
                        'width': '100%',
                        'height': '640',
                    }
                }
            ),
            # 'content': SummernoteInplaceWidget(),
            'tags': forms.CheckboxSelectMultiple(
                attrs={
                    'class': 'custom-btn-check',
                    'id': 'id_tags',
                    'autocomplete': 'off',
                }
            ),
            'is_published': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'id': 'id_published',
                    # 'checked': True,
                }
            ),
        }
