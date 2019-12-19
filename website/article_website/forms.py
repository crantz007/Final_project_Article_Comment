from django import forms
from .models import Comment


class CommentForm(forms.Form):
    class Meta:
        model = Comment
        fields = ['visitor_name', 'visitor_email', 'content']

    visitor_name = forms.CharField(label='Your Name', max_length=50, required=True)
    visitor_email = forms.EmailField(label='Your Email', max_length=100, required=True)
    content = forms.CharField(label='Your Comments', max_length=5000, widget=forms.Textarea)


class SearchForm(forms.Form):
    class Meta:
        fields = ['keywords']

    keywords = forms.CharField(label='Search', max_length=50, required=True)
