from django.db import models
from django.utils.translation import gettext_lazy as _
#from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.utils.text import slugify
from django.utils.html import mark_safe # pip install markupsafe
from ckeditor.fields import RichTextField # pip install django-ckeditor
# from django.utils import timezone
from userauths.models import User
# from taggit.managers import TaggableManager # pip install django-taggit

class Category(models.Model):
    name  = models.CharField(max_length=50, verbose_name=_("name"), default='', help_text='name of catygory')
    slug  = models.SlugField(blank=True, null=True, unique=True, help_text = 'Unique value for category page URL, created from name.')
    image = models.ImageField(upload_to='Category images/', blank=True, null=True, default='category.jpg')
    is_active = models.BooleanField(default=True)
    
    # meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural= 'Categories'
      
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)            
      
    def get_absolute_url(self):
        return reverse('home')
        # return 'https://www.google.fr'
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

VILLE = (
    (1,"Adrar"),
    (2,"Chelef"),
    (3,"Agout"),
    (4,"Oum Bouaghi"),
    (5,"Batna"),
    (6,"Bejaia"),
    (7,"Beskra"),
    (8,"Bechar"),
    (9,"Blida"),
    (10,"Bouira"), 
    (11,"Tamanrasset"),
    (12,"Tébessa"),
    (13,"Tlemcen"),
    (14,"Tiaret"),
    (15,"Tizi Ouzou"),
    (16,"Alger"),
    (17,"Djelfa"),
    (18,"Jijel"),
    (19,"Setif"),
    (20,"Saïda"), 
    (21,"Skikda"),
    (22,"Sidi Bel Abbès"),
    (23,"Annaba"),
    (24,"Guelma"),
    (25,"25.Constantine"),
    (26,"Médéa"),
    (27,"Mostaganem"),
    (28,"M'Sila"),
    (29,"Mascara"),
    (30,"30.Ouargla"), 
    (31,"Oran"),
    (32,"El Bayadh"),
    (33,"Illizi"),
    (34,"Bordj Bou Arreridj"),
    (35,"Boumerdès"),
    (36,"El Tarf"),
    (37,"Tindouf"),
    (38,"Tissemsilt"),
    (39,"El Oued"),
    (40,"Khenchela"), 
    (41,"Souk Ahras"),
    (42,"Tipaza"),
    (43,"Mila"),
    (44,"Aïn Defla"),
    (45,"Naâma"),
    (46,"Aïn Témouchent"),
    (47,"Ghardaïa"),
    (48,"Relizane"),
    (49,"Timimoun"),
    (50,"Bordj Badji Mokhtar"), 
    (51,"Ouled Djellal"),
    (52,"Béni Abbèss"),
    (53,"In Salah"),
    (54,"In Guezzam"),
    (55,"Touggourt "),
    (56,"Djanet"),
    (57,"El Maghaier"),
    (58,"El Menia"),
    
)
class Post(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("User"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category", verbose_name=_("Category"))
    title  = models.CharField(max_length=100, default='', help_text='Title of post', verbose_name = _("title"), unique=True)
    address = models.CharField(max_length=200, default='', help_text='Address of post', verbose_name = _("Address"))
    ville = models.IntegerField(choices = VILLE, verbose_name=_('Ville'))
    email = models.EmailField(max_length=255,blank=True, null=True,  default="", help_text='yourmail@gmail.com', verbose_name=_("Email address"))
    phone  = models.CharField(max_length=20, verbose_name = _("phone")) 
    description = models.TextField(blank=True, null=True, default='', help_text='Informations about your post', verbose_name =_('Description')) #description = RichTextField(blank=True, null=True)
    slug  = models.SlugField(blank=True, null=True, unique=True, help_text = 'Unique value for post page URL, created from name.')
    image = models.ImageField(blank=True, upload_to='post images/', default='post.jpg',  verbose_name=_('Image')) #,default='media/placeholder.png')
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))
    posted_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Posted at')) #, default = timezone.now)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    
    stars = models.IntegerField(default=0, verbose_name=_('Nomber of Stars'))
    stars_begin = models.DateTimeField(blank=True, null=True, verbose_name=_('Stars date'))
    stars_days = models.IntegerField( default=0, verbose_name=_('Stars days'))
    # tags = TaggableManager(blank=True)
    skills = models.CharField(max_length=100, default='', help_text='My skills', verbose_name = _("skills"))
    note  = models.CharField(max_length=1000, null=True,verbose_name = _("note"))

    class Meta:
        db_table = 'postes'
        ordering = ['title']
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)            
             
    def get_absolute_url(self):
        return reverse("app:post-detail", kwargs = {"slug": self.slug})
    #     return reverse('home')
    #     return 'https://www.google.fr'
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def post_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
         
class PostImages(models.Model):
    post  = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, related_name='post', verbose_name=_("post"))
    image = models.ImageField(upload_to='images of post/', default='default_image.jpg') #/%y/%m/%d')
    libellé = models.CharField(max_length=64, blank=True, null=True, verbose_name=_("libellé"))
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.image.name
    
    class Meta:
        verbose_name_plural = "Post images"

# STAR EMOJI
RATING = ( 
    (0, "☆☆☆☆☆"),
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)
class PostReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.CharField(max_length=200, default='', help_text='Review', verbose_name = _("review"))
    rating = models.IntegerField(choices = RATING, default=0)
    date = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        db_table = 'poste reviews'
        ordering = ['-date']
        verbose_name_plural= 'Post Reviews'
 
    def __str__(self):
        return self.post.title
    
    def get_rating(self):
        return self.rating
    
class Wishlist_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'wishlists'
        ordering = ['-date']
        verbose_name_plural= 'wishlists'
        
    def __str__(self):
        return self.post.title
    
class Brand(models.Model):
    name  = models.CharField(max_length=128, verbose_name =_('Name of brand'))
    image = models.ImageField(upload_to='brand', default='brand.jpg', blank=True, verbose_name=_('brand'))
    start = models.DateTimeField(verbose_name=_('Start at'))
    end   = models.DateTimeField(verbose_name=_('End at'))
    is_active = models.BooleanField(default=False)
    slug  = models.SlugField(blank=True,null=True)
   
    def __str__(self):
        return  f"{self.name}"
    
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def brand_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    