from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "image"]

    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout()

        for field in self.Meta().fields:
            helper.layout.append(Field(field, css_class="form-control"))

        return helper


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["description"]
