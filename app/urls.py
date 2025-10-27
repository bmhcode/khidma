# from django.contrib import admin
from django.urls import path

from .views import PostListCreateAPIView, PostDetailAPIView, CategoryList,CategoryCreate, PostList, PostCreate, PostDetail, PostUpdate,PostDelete, post_images_update,post_images_delete,post_images_add,post_delete, wishlist,add_to_wishlist
from django.conf import settings
from django.conf.urls.static import static

#--------------------------------------
# from views import (
#     post_create_view,
#     PostDetailView,
#     post_update
# )
app_name = "app"

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('categories/',CategoryList.as_view(), name="category-list"),
    # path('category-create',category_create, name="category-create"),
    path('category-create',CategoryCreate.as_view(), name="category-create"),
    
    path('posts/', PostListCreateAPIView.as_view(),name='posts-api'),
    path('posts/<int:pk>/',PostDetailAPIView.as_view()),
    
    path('',PostList.as_view(), name="posts"), 
    path('create-post/',PostCreate.as_view(), name="post-create"),
    path('<slug:slug>/',PostDetail.as_view(), name="post-detail"),
    path('post-update/<str:slug>',PostUpdate.as_view(), name="post-update"),
    path('post-delete/<str:slug>',PostDelete.as_view(), name="post-delete"),
    
    
    # path('orders/', OrderListAPIView.as_view()),
    # path('user-orders/', UserOrderListAPIView.as_view()),
    # path('products/info/', ProductInfoAPIView.as_view()),

    path('post-images-add/<str:slug>',post_images_add, name="post-images-add"),
    path('post-images-delete/<str:id>',post_images_delete, name="post-images-delete"),
    path('post-images-update/<str:id>',post_images_update, name="post-images-update"),

    # path('post-add-image/<str:slug>',views.post_add_image, name="post-add-image"),
    # path('post-tag/<slug:tag_slug>',views.tag_list, name="tags"),    
    # Add Review
    # path("ajax-add-review/<slug:slug>", ajax-add-review, name="ajax-add-review")
    
    # path("ajax-add-review/<str:slug>", ajax_add_review, name="ajax-add-review"),
    # # add to wishlist
    path('add-to-wishlist/', add_to_wishlist, name="add-to-wishlist"),
    # # wishlist page
    path("wishlist/", wishlist, name="wishlist"),
    # path("wishlist-delete/<str:pk>", wishlist_delete, name="wishlist-delete"),
    
    # path('about',views.about, name="about"),
    # path('contact',views.contact, name="contact"),
    # path('videos',views.videos, name="videos"),
    
]