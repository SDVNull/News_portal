from IPython.core.release import author
from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["author", "header", "content"]

    # def clean(self):
    #     cleaned_data = super().clean()
    #     description = cleaned_data.get("description")
    #     name = cleaned_data.get("name")
    #
    #     if name == description:
    #         raise ValidationError("Описание не должно быть идентично названию.")
    #
    #     return cleaned_data
