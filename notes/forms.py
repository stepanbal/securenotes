from django import forms
from .models import Category, Post


class AddCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)


class AddPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'body', 'rubric', 'is_secret')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

