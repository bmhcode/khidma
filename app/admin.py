from django.contrib import admin
from .models import Category, Post, PostImages, PostReview, Wishlist_model, Brand


class PostImagesAdmin(admin.TabularInline):
    model = PostImages
    list_display = ['user','post','date'] 
    
class PostReviewAdmin(admin.TabularInline):
    model = PostReview
    list_display = ['user','post','review','rating','date']   
    exclude = ["user",'date']
    

class PostAdmin(admin.ModelAdmin):
    inlines = [PostImagesAdmin ,PostReviewAdmin]

    list_display = ['title','image','post_image','category','is_active']
    exclude = ["slug"] # pour ne pas afficher dans admin 
    
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name','image','category_image', 'is_active']   #['name','category_image','is_active']        
    exclude = ["slug"]

    
class WishlistAdmin(admin.ModelAdmin):
    model = Wishlist_model
    list_display = ['user','post','date']       
   

class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ['name','brand_image','start','end','is_active']     
    exclude = ["slug"]   

admin.site.register(Category,CategoryAdmin)
admin.site.register(Post,PostAdmin)
# admin.site.register(PostReview, PostReviewAdmin)
admin.site.register(Wishlist_model,WishlistAdmin)
admin.site.register(Brand,BrandAdmin)

