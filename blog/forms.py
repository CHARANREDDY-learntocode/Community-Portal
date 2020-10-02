from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Post
        fields = ['title', 'content']

