from dataclasses import fields
from django import forms

from .models import Book, Section, Problem


class BookCreateForm(forms.ModelForm):
    tag = forms.CharField(label="タグ", max_length=50, required=False)

    class Meta:
        model = Book
        fields = ('title', 'description', 'cover',)

    def clean_tag(self):
        tag = self.cleaned_data.get("tag")
        tags_list = tag.split(",")
        return tags_list


class SectionCreateForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('title',)


class ProblemCreateForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('question', 'answer', 'explanation',)
