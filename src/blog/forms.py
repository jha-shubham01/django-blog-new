from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)

        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control content"}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "category",
            "image",
            "tags",  # "author"
        )

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control content"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            # "author": forms.HiddenInput(),
        }
