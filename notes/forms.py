from django import forms
from .models import Category


class AddCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)
