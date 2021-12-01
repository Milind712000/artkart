from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Purchases, CustomOrder
from .categories import category_list

@login_required
def initiate_custom_order(request, s_id):
    artist = User.objects.get(id=s_id)
    corder = CustomOrder(buyer=request.user, seller=artist, title='commission', description='list your requirements here')
    corder.save()
    corder.title = 'Commission #'+str(corder.id)
    corder.save()
    return redirect(reverse('item-custom', kwargs={'pk':corder.id}))


def land_home(request):
    return render(request, 'blog/land-home.html')

def home(request):
    context = {
        'posts': Post.objects.filter(public=True).order_by('-date_posted'),
        'tags': category_list
    }
    return render(request, 'blog/art-home.html', context)

@login_required
def custom_order_list(request):
    context = {
        'posts' : CustomOrder.objects.filter(buyer=request.user.id) | CustomOrder.objects.filter(seller=request.user.id)
    }
    return render(request, 'blog/custom_order_list.html', context)

@login_required
def custom_order_item(request, pk):
    corder = CustomOrder.objects.get(id=pk)
    if corder.buyer != request.user and corder.seller != request.user:
        return redirect('blog-home')
    return render(request, 'blog/custom_order_item.html', {'object' : corder})

def home_filter(request, tagname):
    context = {
        'posts': Post.objects.filter(public=True).filter(category=tagname).order_by('-date_posted'),
        'tags': category_list
    }
    return render(request, 'blog/art-home.html', context)

@login_required
def buy_page(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        obj = Purchases(buyer=request.user,
        seller=post.author,
        title=post.title,
        description=post.description,
        image=post.image,
        category=post.category)
        obj.save()
        return redirect('items-bought')
    return render(request, 'blog/buy_confirm.html', {'post' : post})

@login_required
def my_items(request):
    context = {
        'posts' : Purchases.objects.filter(buyer=request.user.id)
    }
    return render(request, 'blog/item_bought.html', context)

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'image', 'category', 'price', 'public']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'description', 'image', 'category', 'price', 'public']

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
