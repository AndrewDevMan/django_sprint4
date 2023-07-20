from blog.models import Comment, Post, User
from django import forms
from django.utils import timezone


class PostForm(forms.ModelForm):
    '''Form for posts'''
    pub_date = forms.DateTimeField(
        initial=timezone.now(),
        label='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.'),
    )

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
