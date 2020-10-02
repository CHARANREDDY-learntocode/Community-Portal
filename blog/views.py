import json

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import (ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import  LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods

from .models import Post
from .forms import PostCreateForm


class PostListView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-date_posted']


#get the blogs posted by the currently loggedin user
class LoggedinUserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/myposts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user.username)
        return Post.objects.filter(author=user).order_by('-date_posted')



class UserPostListView(ListView):
    model = Post
    template_name = 'posts/userposts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/post_detail.html'



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/create_post.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'posts/update_post.html'
    fields = ['title', 'content']

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/delete_post.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False

@login_required
@require_http_methods(['POST'])
def like_post(request):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=int(request.POST.get('post_id')))
        print(request.POST.get('post_id'))
        if post.author != request.user:
            print("entered")
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user.id)
                print("removed from likes")
            else:
                post.likes.add(request.user.id)
                print("liked")
            try:
                view = request.POST.get('from_article')
                if view == "yes":
                     return HttpResponseRedirect(reverse('blog-homepage'))
                else:
                    return HttpResponseRedirect(reverse('post-detail', args=[str(post.id)]))
            except:
                pass


