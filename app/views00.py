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
from app.forms import CategoryForm,PostForm, PostImagesForm, PostReviewForm
from django.forms import inlineformset_factory
from app.filters import PostFilter

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# API
from app.serializers import PostSerializer
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
# end API

class PostListAPIView(ListAPIView) :
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends  = (DjangoFilterBackend,)
    filterset_class  = PostFilter

# @login_required(login_url='userauths:sign-in') # change sign-in to login
# def index(request):
#     categories = Category.objects.all()
#     # categories = Category.objects.all().annotate(post_count=Count("post"))
#     cat = request.GET.get('cat1')
#     if cat == None:
#         posts = Post.objects.all().order_by("date_created") # .order_by('?') random
#     else:
#         # posts = Post.objects.filter(category__name=cat)
#         posts = Post.objects.filter(Q(category__name__icontains=cat) | 
#                                 Q(title__icontains=cat)
#                                 )

    
class CategoryListView(ListView):
    model = Category
    template_name = 'app/category-list.html' 
class PostListView(ListView):
    model = Post
    template_name = 'app/index.html'  # context_object_name ='post_list'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)       
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_filter_form'] = self.filterset.form
        return context

class PostDetailView(DetailView):
    model = Post
           
def post_add0(request):
    categories = Category.objects.all() # categories = user.category_set.all() 
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                # user=user,
                name=data['category_new']
                )
        else:
            category = None
        for image in images:
            post = Post.objects.create(
                user         =request.user,
                category     =category,
                title        =data['title'],
                address      =data['address'],
                ville        =data['ville'],
                email_address=data['email'],
                description  =data['description'],
                phone        =data['phone'],
                image        =image,
            )
            
        return redirect('app:index')
    context = {'categories': categories}
    return render(request, 'app/post-add.html', context)

def post_create_view(request):
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

def category_create_view(request):
    form = CategoryForm(request.POST or None, request.FILES or None)
    # form.instance.user = request.user
    context = {
        'form':form
    }
    
    if form.is_valid():
        obj = form.save(commit=False) # form.save()
        obj.save()
        messages.success(request, "Thank you! You have successfully created a new category !")
        return redirect('app:category-list') # or form.instance.slug)
    
    template = 'app/category-create.html'
    return render(request, template, context)
def post_update_view(request,slug=None):
    post = get_list_or_404(Post,slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    context = {
        'form' : form 
    }
    if form.is_valid():
        form.save()
        messages.success(request, f"Hey {post.user}, your modification was seccesfully done")
        return redirect('app:post-detail', post.slug)
    
    template = 'app/post-update.html'
    return render(request, template, context)

def post_delete_view(request,slug):
    post = get_list_or_404(Post,slug=slug)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "post deleted")
        return HttpResponseRedirect('/')
    context = {
        'post':post
    }
    template = 'app/post-delete.html'
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
            return redirect('app:post-detail', slug)
    context = {'formset': formset}
    return render(request, 'app/post-images-add.html', context)

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
    return render(request,'app/post-update.html', context)
       
def post_detail111(request,slug):
    post = Post.objects.get(slug=slug)
    reviews = PostReview.objects.filter(post=post).order_by('-date')
    # Getting all reviews related to a post
    average_rating = PostReview.objects.filter(post=post).aggregate(rating=Avg('rating'))
    # Post Review form
    review_form = PostReviewForm()
    
    context = {
        'post' : post,
        'reviews' : reviews,
        'average_rating' : average_rating,
        'review_form' : review_form 
        }
    template_name = 'app/post_detail.html'
    return render(request, template_name, context)

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
    return redirect('app:post_detail<slug:post.slug>')

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


