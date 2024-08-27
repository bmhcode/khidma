from django import forms 
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))# ,"required": True,"size": 10, "title": "Your name"}))
    # email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))

    class Meta:
        model = User
        fields = ['username']
        
    # >>> name = forms.TextInput(attrs={"size": 10, "title": "Your name"})
	# comment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
	# agree = forms.BooleanField()
	# date = forms.DateField()
    # birth_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    
    # BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']
    # class ExampleForm(forms.Form):
    #     birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))

	# value = forms.DecimalField()
    # message = forms.CharField(
    #     max_length = 10,
    #     )
    # email_address = forms.EmailField( 
    #     label="Please enter your email address",
    # )   
    # class ExampleForm(forms.Form):
    # first_name = forms.CharField(initial='Your name')
	# agree = forms.BooleanField(initial=True)
	# day = forms.DateField(initial=datetime.date.today)

    # FAVORITE_COLORS_CHOICES = [
    #     ('blue', 'Blue'),
    #     ('green', 'Green'),
    #     ('black', 'Black'),
    # ]
    # class ExampleForm(forms.Form):
    #     favorite_color = forms.ChoiceField(choices=FAVORITE_COLORS_CHOICES)

    # class ExampleForm(forms.Form):
    #     favorite_color = forms.ChoiceField(widget=forms.RadioSelect, choices=FAVORITE_COLORS_CHOICES)

    # class ExampleForm(forms.Form):
    #     favorite_colors = forms.MultipleChoiceField(choices=FAVORITE_COLORS_CHOICES)

    # class ExampleForm(forms.Form):
    #     favorite_colors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=FAVORITE_COLORS_CHOICES,)


    # from django import forms
    # from .models import MyModel

    # # Create your forms here.

    # class ExampleForm(forms.Form):
    #     model_choice = forms.ModelChoiceField(
    #         queryset = MyModel.objects.all(),
    #         initial = 0
    #         )

    # class ExampleForm(forms.Form):
    #     model_choices = forms.ModelMultipleChoiceField(
    #         widget = forms.CheckboxSelectMultiple,
    #         queryset = MyModel.objects.all(),
    #         initial = 0
    #         )

    # #Rendering Django forms in HTML templates

    # env > mysite > main > views.py

    # from django.shortcuts import render, redirect
    # from .forms import ExampleForm


    # # Create your views here.
    # def contact(request):
    #     form = ExampleForm()
    #     return render(request, "main/contact.html", {'form':form})



