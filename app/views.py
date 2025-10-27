from math import prod
from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_list_or_404
from django.db.models import Count, Avg
from bs4 import Tag
from django.core.paginator import Paginator
from django.db.models import Q
from taggit.models import Tag
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from app.models import Category, Post, PostImages, PostReview, Wishlist_model
from app.forms import CategoryForm, PostForm, PostImagesForm, PostReviewForm
from django.forms import inlineformset_factory

from app.filters import PostFilter
# =============== Class based view ===========================
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.urls import reverse

# ===================== start API =============================
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from app.serializers import PostSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView


class PostListCreateAPIView(ListCreateAPIView) :
    queryset = Post.objects.filter(is_active=True) # Product.objects.filter(stok__gt=0) , Product.objects.exclude(stock__gt=0)
    serializer_class = PostSerializer
    # filter_backends  = [DjangoFilterBackend]
    # filterset_class  = PostFilter
  
class PostDetailAPIView(RetrieveAPIView) :
    queryset = Post.objects.all()
    serializer_class = PostSerializer   
    # lookup_url_kwarg = 'bmh_post_id' # option the same in urls 'posts/<int=bmh_post_id>'


# class OrderListAPIView(ListAPIView) :
#     queryset = Post.objects.prefetch_related('items__post') # ManyToMany
#     serializer_class = PostSerializer
   
# class UserOrderListAPIView(ListAPIView) :
#     queryset = Post.objects.prefetch_related('items__post')
#     serializer_class = PostSerializer
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(user=self.request.user)
    
# class ProductInfoAPIView(APIView) :
#     def get(self, request):
#         products = Product.objects.all()
#         serialiser = ProductInfoSerialiser({
#             'product':products,
#             'count': len(products),
#             'max_price' : products.aggregate(max_price=Max('price')['max_price'])
#         })
 
# ================ End API ================================
  
# def category_create(request):
#     form = CategoryForm(request.POST or None, request.FILES or None)
#     # form.instance.user = request.user
#     context = {
#         'form':form
#     }
#     if form.is_valid():
#         obj = form.save(commit=False) # form.save()
#         obj.save()
#         messages.success(request, "Thank you! You have successfully created a new category !")
#         return redirect('app:category-list') # or form.instance.slug)
    
#     template = 'app/category_create.html'
#     return render(request, template, context)

class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm # fields = '__all__' fields=['name','image']
    # template_name = 'app/category_form.html' # by default
    success_url = reverse_lazy('app:category-list')
    
class CategoryList(ListView):
    model = Category
    # context_object_name ='category_list' # (by default)
    # template_name = 'app/category_list.html' # (by default)
    ordering = 'name' # ordering = ['-posted_at']
    paginate_by = 6
    def get_paginate_by(self, queryset): 
        paginate_by = self.request.GET.get('paginate_by')
        return self.request.GET.get('page_size', self.paginate_by)
    
class PostList(ListView):
    model = Post # queryset = Post.objects.all()
    template_name = 'app/index.html'  # 'app/post_list.html' ( by default)
    context_object_name = 'posts' # ='post_list' ( by default)
    paginate_by = 6
    ordering = 'title' # ordering = ['-posted_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)       
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['posts'] = context['posts'].filter(user=self.request.user)
        # context['count'] = context['posts'].filter(is_active=True).count()
        context['post_filter_form'] = self.filterset.form
        return context


class PostCreate(CreateView):
    model = Post
    form_class = PostForm # fields = '__all__'
    # template_name = 'app/post_form.html'
    def get_success_url(self): 
        return reverse_lazy('app:post-detail',args=[self.object.slug])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class PostDetail(DetailView):
    model = Post
    # template_name = 'app/post_detail.html'
    # context_object_name ='post'
    # pk_url_kwarg = 'post_pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['related_posts'] = Post.objects.filter(category=post.category).exclude(slug=post.slug)[:4]
        # Access related books using self.object.books (related_name)
        # context['category'] = self.object.posts.values('title')
        return context
    
class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm # fields = ['title', 'description', 'complete'] or '__all__'
    # exclude = ['is_active','stars','stars_begin','stars_days','posted_at','updated_at']
    # template_name = 'app/post_form.html' (by default)
   
    def get_success_url(self):  # success_url = reverse_lazy('app:post-detail')
        # Example: Redirect to the detail page of the updated object
        return reverse_lazy('app:post-detail',args=[self.object.slug])
       
class PostDelete(DeleteView):
    model = Post
    # template_name = 'app/post_confirm_delete' # by default
    context_object_name = 'post'
    success_url = reverse_lazy('app:posts') 

def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    form.instance.user = request.user
    context = {
        'form':form
    }
    
    if form.is_valid():
        obj = form.save(commit=False) # form.save()
        obj.save()
        messages.success(request, "Thank you! You have successfully created a new blog post !")
        return redirect('app:post-detail', obj.slug ) # or form.instance.slug)
    template = 'app/post_create.html'
    return render(request, template, context)
  
def post_update(request, slug=None):
    post = get_list_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    context = {
        'form' : form 
    }
    if form.is_valid():
        form.save()
        messages.success(request, f"Hey {post.user}, your modification was seccesfully done")
        return redirect('app:post-detail', post.slug)
    
    template = 'app/post_update.html'
    return render(request, template, context)

def post_delete(request,slug):
    post = get_list_or_404(Post,slug=slug)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "post deleted")
        return HttpResponseRedirect('/')
    context = {
        'post':post
    }
    template = 'app/post_delete.html'
    return render(request,template, context)

def post_images_add(request,slug):
    imageFormSet = inlineformset_factory(Post,PostImages,fields=('image','libellé'), extra=4)
    post = Post.objects.get(slug=slug)
    formset = imageFormSet(instance=post)
    if request.method == 'POST':
        formset = imageFormSet(request.POST, request.FILES, instance=post)
        # form.instance.post = post
        if formset.is_valid():
            formset.save()
            messages.success(request, "Thank you! You have successfully Add your image !")
            return redirect('app:post-detail', post.slug)
    context = {'formset': formset}
    return render(request, 'app/post_images_add.html', context)

def post_images_delete(request,id):
    item = PostImages.objects.get(id=id)
    item.delete()
    messages.success(request, f"Hey {request.user}, your image is deleted")
    return redirect('app:post-detail', item.post.slug )

def post_images_update(request,id):
    img = PostImages.objects.get(id=id)
    form = PostImagesForm(request.POST or None, request.FILES or None, instance=img)
    if form.is_valid():
        form.save()
        messages.success(request, f"Hey {img.post.user}, your modification was seccesfully done")
        return redirect('app:post-detail', img.post.slug)
        
    context = {'img':img, 'form' : form}#, 'message' : message}
    return render(request,'app/post_form.html', context)
 

def ajax_add_review(request,slug):
    post = Post.objects.get(slug=slug)
    user = request.user
    
    review = PostReview.objects.create(
        user = user,
        post = post,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )
    context = {
        'user':user.username,
        'review':request.POST['review'],
        'rating':request.POST['rating'],
    }
    average_reviews = PostReview.objects.filter(post=post).aggregate(rating=Avg('rating'))
    return redirect('app:post-detail<slug:post.slug>')

    # return JsonResponse(
    #     {
    #     'bool':True,
    #     'context':context,
    #     'average_reviews':average_reviews
    #     }
    # )
   
def add_to_wishlist(request):
    post_slug = request.GET.get('post_slug')
    post = Post.objects.get(slug=post_slug)
    
    context = {}
    wishlist_count = Wishlist_model.objects.filter(post=post, user=request.user).count()
    if wishlist_count > 0:
        context = {
            "bool":True
        }
    else:
        new_wishlist = Wishlist_model.objects.create(
            post=post, 
            user=request.user 
            )
        context = {
            "bool":True
            }
    return HttpResponseRedirect('/')    
    # return JsonResponse(context)

# @login_required
def wishlist(request):
    try:
        wishlist = Wishlist_model.objects.filter(user=request.user)
    except:
        wishlist = None
        
    context = {
        'wishlist':wishlist
    }

    return render(request, 'app/wishlist.html', context)

def wishlist_delete(request,pk):
    item = Wishlist_model.objects.get(pk=pk)
    item.delete()
    messages.success(request, f"Hey {request.user}, your post is go out from your wishlist")
    return redirect('app:wishlist')
   
def contact(request):
    context = {}
    return render(request, 'app/contact.html', context)

def videos(request):
    context = {}
    return render(request, 'app/videos.html', context)


