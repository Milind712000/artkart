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
from .forms import bp_0, bp_2, sp_1, sp_12
from datetime import datetime

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

    if corder.buyer == request.user:
        if corder.rejected:
            # order rejected, no more actions
            pass

        elif corder.phase_2:
            # order completed, no more actions
            pass

        elif corder.phase_0 == False:
            if request.method == 'POST':
                form = bp_0(request.POST)
                if form.is_valid():
                    corder.description = form.cleaned_data['desc']
                    corder.price = form.cleaned_data['price']
                    corder.phase_0 = True
                    corder.description_update_date = datetime.now()
                    corder.save()
                    return redirect(reverse('item-custom', kwargs={'pk':corder.id}))
            else:
                form = bp_0()
            return render(request, 'blog/custom_order_item.html', {'object' : corder, 'form' : form})
        
        elif corder.phase_2 == False:
            if request.method == 'POST':
                form = bp_2(request.POST)
                if form.is_valid():
                    if form.cleaned_data['Action'] == 'a':
                        corder.phase_2 = True
                        corder.save()
                        obj = Purchases(buyer=corder.buyer,
                        seller=corder.seller,
                        title=corder.title,
                        description=corder.description,
                        image=corder.image)
                        obj.save()
                        return redirect('items-bought')
                    else:
                        corder.description = corder.description + '\n\n' + str('Changes requested on : ' + datetime.now().strftime("%Y-%m-%d %H:%M")) + '\n' + form.cleaned_data['changes']
                        corder.description_update_date = datetime.now()
                        corder.save()
                        return redirect(reverse('item-custom', kwargs={'pk':corder.id}))
            else:
                form = bp_2(initial={
                    'changes' : 'no changes required',
                    'Action' : 'a'
                })
            return render(request, 'blog/custom_order_item.html', {'object' : corder, 'form' : form})

    elif corder.seller == request.user:
        if corder.rejected:
            # order rejected, no more actions
            pass

        elif corder.phase_2:
            # order completed, no more actions
            pass

        elif corder.phase_0 == True and corder.phase_1 == False:
            if request.method == 'POST':
                form = sp_1(request.POST)
                if form.is_valid():
                    corder.phase_1 = True
                    corder.rejected = form.cleaned_data['Accept'] == 'n'
                    corder.image_update_date = datetime.now()
                    corder.save()
                    return redirect(reverse('item-custom', kwargs={'pk':corder.id}))
            else:
                form = sp_1()
            return render(request, 'blog/custom_order_item.html', {'object' : corder, 'form' : form})
        
        elif corder.phase_1 == True:
            if request.method == 'POST':
                form = sp_12(request.POST, request.FILES)
                if form.is_valid():
                    corder.image = form.cleaned_data['image']
                    corder.image_update_date = datetime.now()
                    corder.save()
                    return redirect(reverse('item-custom', kwargs={'pk':corder.id}))
            else:
                form = sp_12()
            return render(request, 'blog/custom_order_item.html', {'object' : corder, 'form' : form})

    else:
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
