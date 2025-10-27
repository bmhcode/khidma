from rest_framework import serializers
from app.models import Post

class PostSerializer(serializers.ModelSerializer):
    # category_name = serializers.CharField(source = 'category.name')
    # ville    = serializers.CharField(source = 'get_ville_display')
    
    class Meta:
        model = Post
        # fields = ('id','category_name','title','ville')
        fields = ('title','phone','ville')