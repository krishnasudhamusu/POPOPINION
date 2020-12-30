from django import forms
from .models import Confession, Comment


class ConfessionModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 20}))

    class Meta:
        model = Confession
        fields = ('title', 'content', 'image')


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))

    class Meta:
        model = Comment
        fields = ('body',)
