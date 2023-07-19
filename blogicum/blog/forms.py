from django import forms

from .models import Comment, Post, User


class PostForm(forms.ModelForm):
    '''Form for posts'''
    class Meta:
        model = Post
        exclude = ('author', 'is_published',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'text': forms.Textarea(attrs={'rows': '5'}),
        }


class CommentForm(forms.ModelForm):
    '''Form for comments'''
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': '4'}),
        }


class UserForm(forms.ModelForm):
    """Form for users"""
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")
