from rest_framework import serializers
from app.models import Post

class PostSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source = 'category.name')
    ville = serializers.CharField(source = 'get_ville_display')
    def __str__(self):
        pass

    class Meta:
        model = Post
        fields = ('title','category_name','ville')
       