from blog.forms import CommentForm, PostForm, UserForm
from blog.mixins import CommentMixin, UserIsAuthorMixin
from blog.models import Category, Comment, Post, User
from blog.utils import get_queryset_all_post, get_queryset_published_post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blogicum.settings import LIMIT_POST


class PostListView(ListView):
    '''Page with posts on main page'''
    model = Post
    paginate_by = LIMIT_POST
    template_name = 'blog/index.html'
    queryset = get_queryset_published_post()


class PostDetailView(DetailView):
    '''Page with post and comments'''
    model = Post
    template_name = 'blog/detail.html'
    data_post = None

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        self.data_post = get_object_or_404(Post, pk=pk)
        if self.data_post.author == self.request.user:
            return get_queryset_all_post().filter(pk=pk)
        return get_queryset_published_post().filter(pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.data_post.comments.select_related('author')
        return context


class PostUpdateView(LoginRequiredMixin, UserIsAuthorMixin, UpdateView):
    '''Page for edit post'''
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'pk': self.kwargs.get('pk')})


class PostDeleteView(LoginRequiredMixin, UserIsAuthorMixin, DeleteView):
    '''Page for delete post'''
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user})


class PostCreateView(LoginRequiredMixin, CreateView):
    '''Page for create post'''
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user})


class CategoryPostsListView(PostListView):
    '''Page with posts of one category'''
    template_name = 'blog/category.html'

    def get_queryset(self):
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('category_slug'),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs.get('category_slug'),
        )
        return context


class ProfileListView(PostListView):
    '''Page user with him posts'''
    template_name = 'blog/profile.html'
    author = None

    def get_queryset(self):
        self.author = get_object_or_404(
            User,
            username=self.kwargs.get('username')
        )
        if self.author == self.request.user:
            return get_queryset_all_post().filter(author=self.author)
        return super().get_queryset().filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    '''Page for edit user profile'''
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user},
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    '''Page for create comment'''
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    data_post = None

    def dispatch(self, request, *args, **kwargs):
        self.data_post = get_object_or_404(
            Post,
            pk=self.kwargs.get('pk'),
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.data_post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'pk': self.kwargs.get('pk')})


class CommentUpdateView(CommentMixin, UpdateView):
    '''Page for edit comment'''
    form_class = CommentForm


class CommentDeleteView(CommentMixin, DeleteView):
    '''Page for delete comment'''
