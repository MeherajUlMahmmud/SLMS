from django import forms

from .models import *


class PostBookForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields = ('name', 'university', 'department', 'course', 'image', 'author', 'edition', 'description', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['department'].queryset = DepartmentModel.objects.none()
        # self.fields['course'].queryset = CourseModel.objects.none()
