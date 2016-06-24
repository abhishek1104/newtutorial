from django import forms
from .models import SnippetsComments

class CommentForm(forms.ModelForm):
    class Meta:
        model = SnippetsComments
        exclude = ('created','published',)
        #fields = ('comments', 'snippet',)

