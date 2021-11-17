from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from .categories import category_list

def home(request):
    context = {
        'posts': Post.objects.filter(public=True).order_by('-date_posted'),
        'tags': category_list
    }
    return render(request, 'blog/home.html', context)

def home_filter(request, tagname):
    context = {
        'posts': Post.objects.filter(public=True).filter(category=tagname).order_by('-date_posted'),
        'tags': category_list
    }
    return render(request, 'blog/home.html', context)


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'preview_image', 'full_image', 'category', 'price', 'public']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'description', 'preview_image', 'full_image', 'category', 'price', 'public']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
