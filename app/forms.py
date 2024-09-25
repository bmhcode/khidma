from django import forms
from app.models import Post, PostImages, PostReview

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category','title','address','ville','email',
                  'phone',"description",'skills','image') # "__all__"
        labels = {
            # 'user' : 'User',
            'category' : 'Category',
            'title' : 'Title', # 'title':_('title')
            'address' : 'My address',
            'ville' : 'Ville',
            'email' : 'Email',
            'phone' : 'Phone',
            'description' : 'Infos about your post', 
            'skills' : 'skills'
        }
        widgets = {
            # 'user' : forms.Select(attrs={'class':'form-control','placeholder':'user'}), # 'class':'form-select'
            'category' : forms.Select(attrs={'class':'form-control','placeholder':'Select Category', 'label':"cat"}),
            'title' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'title of your post'}),
            'address' : forms.TextInput(attrs={'class':'form-control','placeholder':'your address'}),
            'ville' : forms.Select(attrs={'class':'form-control'}), # forms.SelectMultiple(attrs={'class':'form-control'}),
            'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'your address mail'}),
            'phone' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'your phone'}),
            'description' : forms.Textarea(attrs={'class':'form-control', "cols": 80, "rows": 4, 'placeholder':'infos about your activity'}),
            #'date' : forms.SelectDateWidget(years=range(1976,2024))
            'skills' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'your skills'}),
        }

class PostImagesForm(forms.ModelForm):
    class Meta:
        model = PostImages
        fields = ('image',"libellé")
        
        labels = {
            'libellé' : 'Infos about image', 
        }
        widgets = {
            'libellé' : forms.TextInput(attrs={'class':'form-control'}),
        }

class PostReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Write review"}))
    class Meta:
        model = PostReview
        fields = ["review",'rating'] # '__all__'
        #exclude = ['rating']