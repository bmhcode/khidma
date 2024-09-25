
from django.conf import settings
from django.conf.urls.static import static
#--------------------------------------
from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    # path('',views.index, name="index"), # path('',views.index, name="index"),
    path('',views.PostListView.as_view(), name="index"),
    
    path('api/', views.PostListAPIView.as_view()),
        
    path('post-add',views.post_add, name="post-add"),
    path('post-images-add/<str:slug>',views.post_images_add, name="post-images-add"),
    path('post-images-delete/<str:id>',views.post_images_delete, name="post-images-delete"),
    path('post-images-update/<str:id>',views.post_images_update, name="post-images-update"),
    
    path('post-detail/<str:slug>',views.post_detail, name="post-detail"),
    path('post-update/<str:slug>',views.post_update, name="post-update"),
    path('post-delete/<str:slug>',views.post_delete, name="post-delete"),
    
    # path('post-add-image/<str:slug>',views.post_add_image, name="post-add-image"),
    # path('post-tag/<slug:tag_slug>',views.tag_list, name="tags"),    
    # Add Review
    # path("ajax-add-review/<slug:slug>", ajax-add-review, name="ajax-add-review")
    
    path("ajax-add-review/<str:slug>", views.ajax_add_review, name="ajax-add-review"),
    # add to wishlist
    path('add-to-wishlist/', views.add_to_wishlist, name="add-to-wishlist"),
    # wishlist page
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist-delete/<str:pk>", views.wishlist_delete, name="wishlist-delete"),
    # path('about',views.about, name="about"),
    # path('contact',views.contact, name="contact"),
    # path('videos',views.videos, name="videos"),
    
]