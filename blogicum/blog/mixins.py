from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .models import Comment, Post


class CommentMixin(LoginRequiredMixin):
    '''Mixin for edit and delete comment'''
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs.get('pk'))
        get_object_or_404(
            Post,
            pk=self.kwargs.get('pk'),
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'pk': self.kwargs.get('pk')})


class UserIsAuthorMixin:
    '''Mixin for validation: User is Author'''
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)
