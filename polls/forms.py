from django import forms
from .models import *


class PollForm(forms.ModelForm):
    choice1 = forms.CharField(label='First Choice', max_length=100, min_length=2,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    choice2 = forms.CharField(label='Second Choice', max_length=100, min_length=2,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    choice3 = forms.CharField(label='Third Choice', max_length=100, min_length=2, required=None,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional Choice'}))

    class Meta:
        model = Question
        fields = ['question', 'choice1', 'choice2', 'choice3']
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 20})
        }


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))

    class Meta:
        model = Comment
        fields = ('body',)
