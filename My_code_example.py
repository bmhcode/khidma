'''
from app.forms import BookNameFilterForm

def index(request):
    name  = request.GET.get('name')
    books = Book.objects.all()
    if name:
        books = books.filter(name__icontains = name)
    context = {
        'form': BoukNameFilterForm(),
        'books':books
         }
    return render(request,'index.html', context)
    
'''
# mydata = Member.objects.filter(firstname='Emil').values()

from django.views.generic import ListView
from app.models import Post

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        # Example: Filter articles by a specific author
        author = self.request.GET.get('author')
        if author:
            return Post.objects.filter(author__name=author)
        return Post.objects.all()

from rest_framework.generics import ListAPIView
from app.models import Post
from app.serializers import PostSerializer

class ArticleListAPIView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        # Example: Filter articles by publication date
        queryset = Post.objects.all()
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(publication_date=date)
        return queryset
