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
from app.forms import PostForm, PostImagesForm, PostReviewForm
from django.forms import inlineformset_factory
from app.filters import PostFilter

from django.views.generic.list import ListView

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
#     posts_wishlist = Wishlist_model.objects.all()
    
#     # Set up Pagination
#     P = Paginator(posts, 4)
#     page = request.GET.get('page')
#     posts_in_page = P.get_page(page)
#     nums = "a" * posts_in_page.paginator.num_pages
#     nomber_pages = posts_in_page.paginator.num_pages 
    
#     average_rating = 3.76   # for test
    
#     context = {'categories':categories,'posts':posts,
#                'nums':nums,'nomber_pages':nomber_pages,
#                'posts_in_page':posts_in_page,
#                'posts_wishlist':posts_wishlist,
#                'average_rating':average_rating}
#     return render(request, 'app/index.html', context)


@login_required(login_url='userauths:sign-in') # change sign-in to login
def index(request):
    categories = Category.objects.all()
    
    post_filter = PostFilter(request.GET, queryset = Post.objects.all())
    
    posts_in_wishlist = Wishlist_model.objects.all()

    # Set up Pagination
    posts = post_filter.qs
    P = Paginator(posts, 3)
    page = request.GET.get('page')
    posts_in_page = P.get_page(page)
    nums = "a" * posts_in_page.paginator.num_pages
    nomber_pages = posts_in_page.paginator.num_pages 
    
    average_rating = 3.76   # for test
    
    context = {
               'categories': categories,
               'post_filter_form': post_filter.form,
               'nums': nums,
               'nomber_pages': nomber_pages,
               'posts_in_page': posts_in_page,         
               'posts_in_wishlist': posts_in_wishlist,
               'average_rating': average_rating,
               }
    return render(request, 'app/index.html', context)

class PostListView(ListView):
    queryset = Post.objects.all()
    template_name = 'app/index.html'
    context_object_name ='posts_in_page'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)       
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_filter_form'] = self.filterset.form
        return context
        

def post_add00(request):
    categories = Category.objects.all() # categories = user.category_set.all() 
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                # user=user,
                name=data['category_new'])
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

def post_add0(request):
    submitted = False
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('app:index') 
            return HttpResponseRedirect('/post-add?submitted=True')
    else:
        form = PostForm
        if 'submitted' in request.GET:
            submitted = True
        
    context = {'form':form, 'user':user, 'submitted':submitted}
    return render(request, 'app/post-add.html', context)

def post_add00(request):
    form = PostForm(request.POST, request.FILES or None)
    message = ''
    if form.is_valid():
        form.save()
        form = PostForm()
        message = "We have received your post"
        # return redirect('app:index') 
        return HttpResponseRedirect('/')

    context = {'form' : form, 'message' : message}
    return render(request, 'app/post-add.html', context)

def post_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! You have successfully posted your post !")
            # post = form.instance
            # return HttpResponseRedirect('/')
            return redirect('app:post-detail', form.instance.slug)
    else:
        form = PostForm()
        return render(request, 'app/post-add.html', {'form': form})

# def post_images_add(request,slug):
#     if request.method == 'POST':
#         post = Post.objects.get(slug=slug)
#         form = PostImagesForm(request.POST, request.FILES)
#         form.instance.post = post
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Thank you! You have successfully Add your image !")
#             return redirect('app:post-detail', slug)
#     else:
#         form = PostImagesForm()
#         return render(request, 'app/post-images-add.html', {'form': form})

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
    form = PostImagesForm(request.POST or None,request.FILES or None, instance=img)
    if form.is_valid():
        form.save()
        messages.success(request, f"Hey {img.post.user}, your modification was seccesfully done")
        return redirect('app:post-detail', img.post.slug)
        
    context = {'img':img, 'form' : form}#, 'message' : message}
    return render(request,'app/post-update.html', context)
       
def post_detail(request,slug):
    post = Post.objects.get(slug=slug)
    # post_images = PostImages.objects.filter(post=post)
    related_posts = Post.objects.filter(category = post.category).exclude(slug=slug)
    reviews = PostReview.objects.filter(post=post).order_by('-date')
    # Getting all reviews related to a post
    average_rating = PostReview.objects.filter(post=post).aggregate(rating=Avg('rating'))
    # Post Review form
    review_form = PostReviewForm()
    
    context = {
        'post' : post,
        # 'post_images' : post_images,
        'related_posts' : related_posts,
        'reviews' : reviews,
        'average_rating' : average_rating,
        'review_form' : review_form,
        }
    return render(request, 'app/post-detail.html', context)

def post_update(request,slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, f"Hey {post.user}, your modification was seccesfully done")
        return redirect('app:post-detail', post.slug)
        # return HttpResponseRedirect('/')
        
    context = { 'post' : post, 'form' : form } #, 'message' : message}
    return render(request, 'app/post-update.html', context)

def post_delete(request,slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        post.delete()
        messages.success(request, f"Hey {post.user}, your post was deleted")
        # return redirect('app:index')
        return HttpResponseRedirect('/')
    return render(request,'app/post-delete.html')
    
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

                
# def tag_list(request,tag_slug=None):
#     posts = Post.objects.filter().oreder_by()
#     tag=None
#     if tag_slug:
#         tag = get_object_or_404(Tag,slug=tag_slug)
#         posts = posts.filter(tags__in=[tag])
#     context = {
#         'posts' : posts,
#         'tag' : tag
#     }
#     return render(request,"app:tag.html", context)


