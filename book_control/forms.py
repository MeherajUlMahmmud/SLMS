from django import forms

from .models import *


class PostBookForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields = ('name', 'university', 'department', 'course', 'image', 'author', 'edition', 'description', 'price')
