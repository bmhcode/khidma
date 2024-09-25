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