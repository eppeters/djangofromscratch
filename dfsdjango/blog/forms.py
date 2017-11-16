from django import forms

class CommentForm(forms.Form):
    author = forms.CharField(max_length=64)
    body = forms.CharField(widget=forms.Textarea, max_length=1024)
